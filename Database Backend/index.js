require('dotenv').config();

const express = require('express');
const { Pool } = require('pg'); 
const cors = require('cors');

const app = express();
const port = 3002;


const pool = new Pool({
  user: process.env.PGUSER,
  //host: process.env.PGHOST,
  //host: "172.28.112.1",
  host: "postgres_db",
  database: process.env.PGDATABASE,
  password: process.env.PGPASSWORD,
  port: process.env.PGPORT,
});



app.use(cors());
app.use(express.json()); // To parse JSON bodies


app.get('/api/transaction_risk_profiles', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM transaction_risk_profiles ORDER BY "generated_at" DESC LIMIT 10');
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

app.get('/api/customer_risk_profiles', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM customer_risk_profiles ORDER BY "CREATED_AT" DESC LIMIT 10');
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});


app.listen(port, () => {
  console.log(`Backend server listening at http://localhost:${port}`);
});



function buildTransactionQuery(options, table_name) {
  
  const { limit, offset, search } = options;
  let whereClause = '';
  const values = [];
  let parameterIndex = 1; 

  if (search && search.trim().length > 0) {
    
    whereClause = `
      WHERE 
        (
          "from_name" ILIKE $${parameterIndex} OR 
          "from_account" ILIKE $${parameterIndex}

        )
    `;
    
    values.push(`%${search.trim()}%`);
    parameterIndex++;
  }

  let query = `
    SELECT 
      * FROM 
      "${table_name}"
    ${whereClause} 
    ORDER BY 
      "generated_at" DESC 
  `;

  const limitValue = limit ? parseInt(limit, 10) : undefined;
  const offsetValue = offset ? parseInt(offset, 10) : undefined;
  
  if (limitValue !== undefined && !isNaN(limitValue)) {
    query += ` LIMIT $${parameterIndex}`;
    values.push(limitValue);
    parameterIndex++;
  } else {
    
    query += ` LIMIT 10`;
  }

  if (offsetValue !== undefined && !isNaN(offsetValue)) {
    query += ` OFFSET $${parameterIndex}`;
    values.push(offsetValue);
    parameterIndex++;
  }

  return {
    query: query.trim(),
    values,
  };
}


app.get('/api/transaction_risk_profiles/filter', async (req, res) => {
  const TABLE_NAME = "transaction_risk_profiles"
  try {
    const options = req.query;

    const { query, values } = buildTransactionQuery(options, TABLE_NAME);
    
    //console.log('SQL Query:', query);
    //console.log('SQL Values:', values);

    const result = await pool.query(query, values);
    
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});


function buildCustomerQuery(options, table_name) {
  
  const { limit, offset, search } = options;
  let whereClause = '';
  const values = [];
  let parameterIndex = 1; 

  if (search && search.trim().length > 0) {
    
    whereClause = `
      WHERE 
        (
          "Full_Name" ILIKE $${parameterIndex} OR 
          "Account_No" ILIKE $${parameterIndex}

        )
    `;
    
    values.push(`%${search.trim()}%`);
    parameterIndex++;
  }

  let query = `
    SELECT 
      * FROM 
      "${table_name}"
    ${whereClause} 
    ORDER BY 
      "UPDATED_AT" DESC 
  `;

  const limitValue = limit ? parseInt(limit, 10) : undefined;
  const offsetValue = offset ? parseInt(offset, 10) : undefined;
  
  if (limitValue !== undefined && !isNaN(limitValue)) {
    query += ` LIMIT $${parameterIndex}`;
    values.push(limitValue);
    parameterIndex++;
  } else {
    
    query += ` LIMIT 10`;
  }

  if (offsetValue !== undefined && !isNaN(offsetValue)) {
    query += ` OFFSET $${parameterIndex}`;
    values.push(offsetValue);
    parameterIndex++;
  }

  return {
    query: query.trim(),
    values,
  };
}




app.get('/api/customer_risk_profiles/filter', async (req, res) => {
  const TABLE_NAME = "customer_risk_profiles"
  try {
    const options = req.query;

    const { query, values } = buildCustomerQuery(options, TABLE_NAME);
    
    //console.log('SQL Query:', query);
    //console.log('SQL Values:', values);

  
    const result = await pool.query(query, values);
    
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});