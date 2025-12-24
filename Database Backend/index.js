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
app.use(express.json()); 


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



function buildTransactionQuery(options, table_name, count=false) {
  
  const { limit, offset, search, risk_filter } = options;
  console.log("Options: ", options)
  let whereClause = '';
  const values = [];
  let parameterIndex = 1; 

  let filterText = "";

  const riskLevel = risk_filter ? (risk_filter === "LOW" ? [0, 50] 
                                    : (risk_filter === "MEDIUM" ? [50, 70] 
                                        : (risk_filter === "HIGH" ? [70, 85] 
                                            : (risk_filter === "CRITICAL" ? [85, 1000] 
                                                : undefined
                                              )
                                            )
                                          )
                                        ) 
                                  : undefined;
    console.log("RiskLevel: ", riskLevel, "Bool", riskLevel !== undefined)

    if (riskLevel !== undefined) {
      console.log("Entered....")
      filterText += `"overall_risk_score" >= $${parameterIndex} AND "overall_risk_score" <= $${parameterIndex + 1}`;
      values.push(riskLevel[0], riskLevel[1]);
      parameterIndex +=2 ;
    }

    console.log("FilterText: ", filterText)



  if ((search && search.trim().length > 0) || riskLevel) {
    
    whereClause = `
      WHERE 
        (
          ${riskLevel? filterText : "1"}
          OR
          "from_name" ILIKE $${parameterIndex} OR 
          "from_account" ILIKE $${parameterIndex}

        )
    `;
    
    values.push(`%${search.trim()}%`);
    parameterIndex++;
  }

  let query = `
    SELECT 
      ${count? "count(*)":"*"} FROM 
      "${table_name}"
    ${whereClause}
    ${
      count ? "" : 
      riskLevel ? `
      ORDER BY 
      "overall_risk_score" DESC,
      "generated_at" DESC
      `:
      `
      ORDER BY 
      "generated_at" DESC
      ` 
    } 
     
  `;

  const limitValue = limit ? parseInt(limit, 10) : undefined;
  const offsetValue = offset ? parseInt(offset, 10) : undefined;
  
  if (limitValue !== undefined && !isNaN(limitValue)) {
    query += ` LIMIT $${parameterIndex}`;
    values.push(limitValue);
    parameterIndex++;
  } else {
    
    //query += ` LIMIT 10`;
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
    
    console.log('SQL Query:', query);
    console.log('SQL Values:', values);

    const result = await pool.query(query, values);
    
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});


app.get('/api/transaction_risk_profiles/count', async (req, res) => {
  const TABLE_NAME = "transaction_risk_profiles"
  try {
    const options = req.query;

    const { query, values } = buildTransactionQuery(options, TABLE_NAME, count=true);
    
    //console.log('SQL Query:', query);
    //console.log('SQL Values:', values);

    const result = await pool.query(query, values);
    
    res.json(result.rows);

  } catch (err) {
    console.error('Error executing query', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});



function buildCustomerQuery(options, table_name, count=false) {
  
  const { limit, offset, search, risk_filter} = options;
  let whereClause = '';
  const values = [];
  let parameterIndex = 1; 

  let filterText = "";

  const riskLevel = risk_filter ? (risk_filter === "LOW" ? [0, 50] 
                                    : (risk_filter === "MEDIUM" ? [50, 70] 
                                        : (risk_filter === "HIGH" ? [70, 85] 
                                            : (risk_filter === "CRITICAL" ? [85, 1000] 
                                                : undefined
                                              )
                                            )
                                          )
                                        ) 
                                  : undefined;

  if (riskLevel !== undefined) {
    filterText += `"RISK_SCORE" >= $${parameterIndex} AND "overall_risk_score" <= $${parameterIndex + 1}`;
    values.push(riskLevel[0], riskLevel[1]);
    parameterIndex +=2;
  }



  if ((search && search.trim().length > 0) || riskLevel) {
    
    whereClause = `
      WHERE 
        (
          ${riskLevel? filterText : "1"}
          OR
          "Full_Name" ILIKE $${parameterIndex} OR 
          "Account_No" ILIKE $${parameterIndex}
        )
    `;
    
    values.push(`%${search.trim()}%`);
    parameterIndex++;
  }

  let query = `
    SELECT 
      ${count? "count(*)":"*"} FROM 
      "${table_name}"
    ${whereClause}
    ${
      count ? "" : 
      riskLevel ? `
      ORDER BY 
      "RISK_SCORE" DESC,
      "CREATED_AT" DESC
      `:
      `
      ORDER BY 
      "CREATED_AT" DESC
      `
    } 
     
  `;

  const limitValue = limit ? parseInt(limit, 10) : undefined;
  const offsetValue = offset ? parseInt(offset, 10) : undefined;
  
  
  if (limitValue !== undefined && !isNaN(limitValue)) {
    query += ` LIMIT $${parameterIndex}`;
    values.push(limitValue);
    parameterIndex++;
  } else {
    
    //query += ` LIMIT 10`;
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


app.get('/api/customer_risk_profiles/count', async (req, res) => {
  const TABLE_NAME = "customer_risk_profiles"
  try {
    const options = req.query;

    const { query, values } = buildCustomerQuery(options, TABLE_NAME, count=true);
    
    //console.log('SQL Query:', query);
    //console.log('SQL Values:', values);

  
    const result = await pool.query(query, values);
    
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err);
    res.status(500).json({ error: 'Database query failed' });
  }
});