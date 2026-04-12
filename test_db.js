import fs from "fs";
import path from "path";
import { parse } from "csv-parse/sync";
import Database from "better-sqlite3";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log("Testing data loading...");

// Load and Clean Data
const csvData = fs.readFileSync(path.join(__dirname, "cleaned_marketing_data.csv"), "utf-8");
const records = parse(csvData, {
  columns: true,
  skip_empty_lines: true,
  cast: true,
});

console.log(`Loaded ${records.length} records from CSV`);

// Initialize SQLite Database
const db = new Database(":memory:");

// Create Table
db.exec(`
  CREATE TABLE customers (
    ID INTEGER PRIMARY KEY,
    Year_Birth INTEGER,
    Education TEXT,
    Marital_Status TEXT,
    Income REAL,
    Kidhome INTEGER,
    Teenhome INTEGER,
    Dt_Customer TEXT,
    Recency INTEGER,
    MntWines REAL,
    MntFruits REAL,
    MntMeatProducts REAL,
    MntFishProducts REAL,
    MntSweetProducts REAL,
    MntGoldProds REAL,
    NumDealsPurchases INTEGER,
    NumWebPurchases INTEGER,
    NumCatalogPurchases INTEGER,
    NumStorePurchases INTEGER,
    NumWebVisitsMonth INTEGER,
    AcceptedCmp3 INTEGER,
    AcceptedCmp4 INTEGER,
    AcceptedCmp5 INTEGER,
    AcceptedCmp1 INTEGER,
    AcceptedCmp2 INTEGER,
    Response INTEGER,
    Complain INTEGER,
    Country TEXT,
    Age INTEGER,
    Total_Spend REAL,
    Total_Purchases INTEGER,
    Children INTEGER,
    Primary_Segment TEXT
  )
`);

// Insert data
const insert = db.prepare(`
  INSERT INTO customers (
    ID, Year_Birth, Education, Marital_Status, Income, Kidhome, Teenhome, Dt_Customer, Recency,
    MntWines, MntFruits, MntMeatProducts, MntFishProducts, MntSweetProducts, MntGoldProds,
    NumDealsPurchases, NumWebPurchases, NumCatalogPurchases, NumStorePurchases, NumWebVisitsMonth,
    AcceptedCmp3, AcceptedCmp4, AcceptedCmp5, AcceptedCmp1, AcceptedCmp2, Response, Complain, Country,
    Age, Total_Spend, Total_Purchases, Children, Primary_Segment
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

records.forEach((r: any) => {
  insert.run(
    r.ID, r.Year_Birth, r.Education, r.Marital_Status, r.Income, r.Kidhome, r.Teenhome, r.Dt_Customer, r.Recency,
    r.MntWines, r.MntFruits, r.MntMeatProducts, r.MntFishProducts, r.MntSweetProducts, r.MntGoldProds,
    r.NumDealsPurchases, r.NumWebPurchases, r.NumCatalogPurchases, r.NumStorePurchases, r.NumWebVisitsMonth,
    r.AcceptedCmp3, r.AcceptedCmp4, r.AcceptedCmp5, r.AcceptedCmp1, r.AcceptedCmp2, r.Response, r.Complain, r.Country,
    r.Age, r.Total_Spend, r.Total_Purchases, r.Children, r.Primary_Segment
  );
});

console.log("Data inserted into database");

// Test queries
const totalCustomers = db.prepare("SELECT COUNT(*) as count FROM customers").get() as any;
const avgSpend = db.prepare("SELECT AVG(Total_Spend) as avg FROM customers").get() as any;
const segments = db.prepare("SELECT Primary_Segment, COUNT(*) as count FROM customers GROUP BY Primary_Segment").all();

console.log("Total customers:", totalCustomers.count);
console.log("Average spend:", avgSpend.avg);
console.log("Segments:", segments);

db.close();
console.log("Test completed successfully!");