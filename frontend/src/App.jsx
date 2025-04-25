import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [items, setItems] = useState([])
  const [newItem, setNewItem] = useState('')
  const [count, setCount] = useState(0)

  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${API_URL}/items`)
      const data = await response.json()
      setItems(data)
    } catch (error) {
      console.error('Error fetching items:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${API_URL}/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newItem }),
      })
      const data = await response.json()
      setItems([...items, data])
      setNewItem('')
    } catch (error) {
      console.error('Error creating item:', error)
    }
  }

  return (
    <div className="container">
      <h1>Test Web App</h1>
      
      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="Enter new item"
          required
        />
        <button type="submit">Add Item</button>
      </form>

      <ul className="items-list">
        {items.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  )
}

export default App
