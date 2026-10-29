const API_URL = 'http://127.0.0';

// DOM Elements
const expenseForm = document.getElementById('expense-form');
const expenseIdInput = document.getElementById('expense-id');
const descriptionInput = document.getElementById('description');
const amountInput = document.getElementById('amount');
const categoryInput = document.getElementById('category');

const formTitle = document.getElementById('form-title');
const btnSubmitText = document.getElementById('btn-submit-text');
const btnCancel = document.getElementById('btn-cancel');
const tableBody = document.getElementById('expenses-table-body');
const warningMessage = document.getElementById('warning-message');

let isEditMode = false;

// 2. VIEW: Fetch all expenses from backend
async function fetchExpenses() {
    try {
        const response = await fetch(API_URL);
        const expenses = await response.json();
        renderTable(expenses);
    } catch (error) {
        console.error('Error fetching expenses:', error);
    }
}

// Render data rows dynamically into the DOM
function renderTable(expenses) {
    tableBody.innerHTML = '';
    if (expenses.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">No expenses tracked yet.</td></tr>`;
        return;
    }

    expenses.forEach(exp => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${exp.id}</td>
            <td>${exp.description}</td>
            <td>${exp.category}</td>
            <td>$${exp.amount.toFixed(2)}</td>
            <td>
                <button class="btn-edit" onclick="setupEditMode(${exp.id}, '${exp.description}', ${exp.amount}, '${exp.category}')">Edit</button>
                <button class="btn-delete" onclick="deleteExpense(${exp.id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// 1 & 3. ADD and UPDATE form submission handler
expenseForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const amount = parseFloat(amountInput.value);

    // Dynamic Validation Check: Zero or negative check
    if (amount <= 0) {
        warningMessage.textContent = 'Warning: Expense amount must be greater than zero!';
        warningMessage.classList.remove('hidden');
        amountInput.focus();
        return; // Terminate execution early to prevent API submission
    }

    // Hide warning message if the validation passes
    warningMessage.classList.add('hidden');

    const expenseData = {
        description: descriptionInput.value,
        amount: amount,
        category: categoryInput.value
    };

    try {
        if (isEditMode) {
            // 3. UPDATE execution
            const id = expenseIdInput.value;
            await fetch(`${API_URL}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expenseData)
            });
        } else {
            // 1. ADD execution
            await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expenseData)
            });
        }
        
        resetForm();
        fetchExpenses();
    } catch (error) {
        console.error('Error processing expense request:', error);
    }
});

// 4. DELETE execution
async function deleteExpense(id) {
    if (confirm('Are you sure you want to remove this expense?')) {
        try {
            await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
            if (isEditMode && expenseIdInput.value == id) {
                resetForm();
            }
            fetchExpenses();
        } catch (error) {
            console.error('Error deleting expense:', error);
        }
    }
}

// Transition UI into edit state
function setupEditMode(id, description, amount, category) {
    isEditMode = true;
    formTitle.textContent = 'Edit Expense';
    btnSubmitText.textContent = 'Save Changes';
    btnCancel.classList.remove('hidden');
    warningMessage.classList.add('hidden'); // Clear warnings on mode change

    expenseIdInput.value = id;
    descriptionInput.value = description;
    amountInput.value = amount;
    categoryInput.value = category;
}

// Revert form state back to regular Add Mode
function resetForm() {
    isEditMode = false;
    formTitle.textContent = 'Add New Expense';
    btnSubmitText.textContent = 'Add Expense';
    btnCancel.classList.add('hidden');
    warningMessage.classList.add('hidden'); // Clear warnings
    
    expenseForm.reset();
    expenseIdInput.value = '';
}

btnCancel.addEventListener('click', resetForm);

// Initial Data Fetch on app start
fetchExpenses();
