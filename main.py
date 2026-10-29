from fastapi import FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from typing import List, Optional
import  uvicorn
import  nest_asyncio

app = FastAPI(title="My Expense Tracker API")

# Enable CORS so our frontend HTML file can communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database counters and storage
expense_id_counter = 1
expenses_db = []

# Pydantic Schemas
class ExpenseBase(BaseModel):
    description: str
    amount: float = Field(...,gt=0,description ="The expense Amount must  be  greater  than  0 (Zero)")
    category: str
    

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int

# 1. Add Expense (POST)
@app.post("/expenses", response_model=Expense, status_code=201)
async def create_expense(expense: ExpenseCreate):
      #check  if the amount is 0  or less
    if  expense.amount <=0: 
           raise HTTPException (
                status_code = status.HTTP_400_BAD_REQUEST,
                detail ="Warning : Expense  ammount  must be greater  than  0(Zero)"
             )
    global expense_id_counter
    new_expense = Expense(
              id=expense_id_counter,
              description=expense.description,
              amount=expense.amount,
              category=expense.category
      )
    expenses_db.append(new_expense)
    expense_id_counter += 1
    return new_expense

# 2. View Expenses (GET)
@app.get("/expenses", response_model=List[Expense])
def get_expenses():
    return expenses_db

# 3. Update Expense (PUT)
@app.put("/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, updated_data: ExpenseCreate):
    for index, expense in enumerate(expenses_db):
        if expense.id == expense_id:
            updated_expense = Expense(
                id=expense_id,
                description=updated_data.description,
                amount=updated_data.amount,
                category=updated_data.category
            )
            expenses_db[index] = updated_expense
            return updated_expense
    raise HTTPException(status_code=404, detail="Expense not found")

# 4. Delete Expense (DELETE)
@app.delete("/expenses/{expense_id}", status_code=200)
def delete_expense(expense_id: int):
    for index, expense in enumerate(expenses_db):
        if expense.id == expense_id:
            expenses_db.pop(index)
            return {"Message " : f"Expense with ID '{expense_id}' deleted successfully "}
    
    raise HTTPException(status_code=404, detail="Expense not found")

#  5. Get total spending on items
@app.get("/analytics/total")
def get_total_spending():
      total = sum (expense.amount for expense in expenses_db)

      return {

              "Total_spending":  total, 
              "Total_items":len(expenses_db)
       }


#6.Filter Expenses  by  Category  given at  the  time of creating
@app.get("/analytic/filter")
def filter_by_category(category:str):
      filtered_expenses = [
           expense for expense in  expenses_db
           if expense.category.strip().lower() == category.strip().lower()
   
     ]
      return  filtered_expenses


nest_asyncio.apply()

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="127.0.0.1", port=8500, reload=False)
