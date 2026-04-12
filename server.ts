import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";
import { parse } from "csv-parse/sync";
import Database from "better-sqlite3";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const PORT = 3000;

  // Initialize SQLite Database
  const db = new Database(":memory:");

  // Load and Clean Data
  const csvData = fs.readFileSync(path.join(__dirname, "cleaned_marketing_data.csv"), "utf-8");
  const records = parse(csvData, {
    columns: true,
    skip_empty_lines: true,
    cast: true,
  });

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

  // API Routes
  app.get("/api/stats", (req, res) => {
    const totalCustomers = db.prepare("SELECT COUNT(*) as count FROM customers").get() as any;
    const avgSpend = db.prepare("SELECT AVG(Total_Spend) as avg FROM customers").get() as any;
    const responseRate = db.prepare("SELECT (SUM(Response) * 100.0 / COUNT(*)) as rate FROM customers").get() as any;
    const avgIncome = db.prepare("SELECT AVG(Income) as avg FROM customers WHERE Income > 0").get() as any;

    res.json({
      totalCustomers: totalCustomers.count,
      avgSpend: avgSpend.avg,
      responseRate: responseRate.rate,
      avgIncome: avgIncome.avg
    });
  });

  app.get("/api/segments", (req, res) => {
    const segments = db.prepare(`
      SELECT Primary_Segment as Segment, COUNT(*) as count, AVG(Total_Spend) as avgSpend, AVG(Response) * 100 as responseRate
      FROM customers 
      GROUP BY Primary_Segment
    `).all();
    res.json(segments);
  });

  app.get("/api/spending-by-category", (req, res) => {
    const data = db.prepare(`
      SELECT 
        AVG(MntWines) as Wines, 
        AVG(MntFruits) as Fruits, 
        AVG(MntMeatProducts) as Meat, 
        AVG(MntFishProducts) as Fish, 
        AVG(MntSweetProducts) as Sweets, 
        AVG(MntGoldProds) as Gold
      FROM customers
    `).get();
    res.json(data);
  });

  app.get("/api/response-by-campaign", (req, res) => {
    const data = db.prepare(`
      SELECT 
        SUM(AcceptedCmp1) as Cmp1,
        SUM(AcceptedCmp2) as Cmp2,
        SUM(AcceptedCmp3) as Cmp3,
        SUM(AcceptedCmp4) as Cmp4,
        SUM(AcceptedCmp5) as Cmp5,
        SUM(Response) as LastResponse
      FROM customers
    `).get();
    res.json(data);
  });

  app.get("/api/customers", (req, res) => {
    const customers = db.prepare("SELECT * FROM customers LIMIT 100").all();
    res.json(customers);
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
