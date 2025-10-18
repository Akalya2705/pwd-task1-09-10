import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [todos, setTodos] = useState([])
  const [input, setInput] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    fetchTodos()
  }, [])

  const fetchTodos = async () => {
    try {
      const res = await fetch('/api/todos')
      const data = await res.json()
      setTodos(data)
    } catch (err) {
      setError('Cannot connect to server')
    }
  }

  const addTodo = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    try {
      const res = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: input })
      })
      const newTodo = await res.json()
      setTodos([newTodo, ...todos])
      setInput('')
    } catch (err) {
      setError('Failed to add todo')
    }
  }

  const toggleTodo = async (id, completed) => {
    try {
      const res = await fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !completed })
      })
      const updated = await res.json()
      setTodos(todos.map(t => t._id === id ? updated : t))
    } catch (err) {
      setError('Failed to update')
    }
  }

  const deleteTodo = async (id) => {
    try {
      await fetch(`/api/todos/${id}`, { method: 'DELETE' })
      setTodos(todos.filter(t => t._id !== id))
    } catch (err) {
      setError('Failed to delete')
    }
  }

  const stats = {
    total: todos.length,
    completed: todos.filter(t => t.completed).length,
    pending: todos.filter(t => !t.completed).length
  }

  return (
    <div className="container">
      <h1>📝 My Todo List</h1>
      
      {error && <div className="error">{error}</div>}
      
      <form onSubmit={addTodo}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Add a new todo..."
        />
        <button type="submit">Add</button>
      </form>

      <ul className="todo-list">
        {todos.map(todo => (
          <li key={todo._id} className={todo.completed ? 'completed' : ''}>
            <div className="todo-content">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleTodo(todo._id, todo.completed)}
              />
              <span>{todo.title}</span>
            </div>
            <button onClick={() => deleteTodo(todo._id)} className="delete">
              🗑️
            </button>
          </li>
        ))}
      </ul>

      <div className="stats">
        <span>Total: {stats.total}</span>
        <span>Completed: {stats.completed}</span>
        <span>Pending: {stats.pending}</span>
      </div>
    </div>
  )
}

export default App
