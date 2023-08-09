from fastapi import FastAPI, HTTPException
import database

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": """Welcome to the Stock API!
        To get all stocks, go to /stock
        To get a stock by its symbol, go to /stock/{stock_symbol}
        To get a stock by its id, go to /stock/id/{id}
        To create a stock, go to /stock
        To delete a stock by its symbol, go to /stock/{stock_symbol}
        To delete all stocks, go to /stock
        To update a stock by its symbol, go to /stock/{stock_symbol}
        To update all stocks, go to /stock
        """
    }

@app.get("/stock")
def read_all():
    db = database.connect()
    if db.is_connected():
        db = database.connect()
        result = database.select_all(db)
        return result
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    db.close()

@app.get("/stock/{stock_symbol}")
def read_by_symbol(stock_symbol: str):
    if not stock_symbol:
        raise HTTPException(status_code=404, detail="Item not found")
    db = database.connect()
    result = database.select_by_symbol(db, stock_symbol)
    return result

    db.close()

@app.get("/stock/id/{id}")
def read_by_id(id: int):
    if not id:
        raise HTTPException(status_code=404, detail="Item not found")
    db = database.connect()
    result = database.select_by_id(db, id)
    return result

    db.close()

@app.post("/stock")
def create(stock_industry: str, stock_market: str, stock_name: str, stock_market_cap: str, stock_symbol: str):
    if type(stock_industry) != str or type(stock_market) != str or type(stock_name) != str or type(stock_market_cap) != str or type(stock_symbol) != str:
        raise HTTPException(status_code=400, detail="Invalid data type")
    db = database.connect()
    result = database.insert(db, stock_industry, stock_market, stock_name, stock_market_cap, stock_symbol)
    return {
        "message": "Stock created successfully"
    }

    db.close()

@app.delete("/stock/{stock_symbol}")
def delete(stock_symbol: str):
    db = database.connect()
    if not stock_symbol:
        raise HTTPException(status_code=404, detail="Item not found")
    result = database.delete_by_symbol(db, stock_symbol)
    return {
        "message": "Stock deleted successfully"
    }

    db.close()

@app.delete("/stock")
def delete_all():
    db = database.connect()
    if db.is_connected():
        result = database.delete_all(db)
        return {
            "message": "All stocks has been deleted successfully"
        }
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    db.close()

@app.put("/stock/{stock_symbol}")
def update(stock_industry: str, stock_market: str, stock_name: str, stock_market_cap: str, stock_symbol: str):
    if not stock_symbol:
        raise HTTPException(status_code=404, detail="Item not found")
    db = database.connect()
    result = database.update_by_symbol(db, stock_industry, stock_market, stock_name, stock_market_cap, stock_symbol)
    return {
        "message": "Stock updated successfully"
    }
    db.close()

@app.put("/stock")
def update_all(stock_industry: str, stock_market: str, stock_name: str, stock_market_cap: str, stock_symbol: str):
    db = database.connect()
    if db.is_connected():
        result = database.update_all(db, stock_industry, stock_market, stock_name, stock_market_cap, stock_symbol)
        return {
            "message": "All stocks has been updated successfully"
        }
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    db.close()

