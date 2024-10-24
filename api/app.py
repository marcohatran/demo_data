from fastapi import FastAPI
import asyncpg

app = FastAPI()

async def get_db_conn():
    return await asyncpg.connect(user='postgres', password='postgres',
                                 database='poc_stream', host='ip')

@app.get("/leads")
async def get_leads():
    conn = await get_db_conn()
    leads = await conn.fetch("SELECT * FROM insights.leads ORDER BY processed_timestamp DESC LIMIT 100")
    await conn.close()
    return leads

@app.get("/metrics")
async def get_metrics():
    conn = await get_db_conn()
    total_leads = await conn.fetchval("SELECT COUNT(*) FROM insights.leads")
    top_sales_reps = await conn.fetch("SELECT sales_rep_name as sales_name, COUNT(*) FROM insights.leads GROUP BY sales_rep_name ORDER BY COUNT(*) DESC")
    product_interest = await conn.fetch("SELECT product_name, COUNT(*) FROM insights.leads GROUP BY product_name")
    await conn.close()

    return {
        "total_leads": total_leads,
        "top_sales_reps": top_sales_reps,
        "product_interest": product_interest
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
