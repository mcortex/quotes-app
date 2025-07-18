<template>
  <div id="app">
    <header>
      <h1>Quotes & Characters Manager</h1>
    </header>

    <main>
      <!-- Characters Section -->
      <section class="section">
        <h2>Characters</h2>
        <div class="form-group">
          <input v-model="newCharacter.name" placeholder="Character name" @keyup.enter="createCharacter" />
          <button @click="createCharacter" :disabled="!newCharacter.name">
            Add Character
          </button>
        </div>

        <div class="items-grid">
          <div v-for="character in characters" :key="character.id" class="item-card">
            <span>{{ character.name }}</span>
            <button @click="deleteCharacter(character.id)" class="delete-btn">
              Delete
            </button>
          </div>
        </div>
      </section>

      <!-- Quotes Section -->
      <section class="section">
        <h2>Quotes</h2>
        <div class="form-group">
          <textarea v-model="newQuote.quote" placeholder="Enter quote..." rows="3"></textarea>
          <select v-model="newQuote.character_id">
            <option value="">Select character</option>
            <option v-for="character in characters" :key="character.id" :value="character.id">
              {{ character.name }}
            </option>
          </select>
          <button @click="createQuote" :disabled="!newQuote.quote || !newQuote.character_id">
            Add Quote
          </button>
        </div>

        <div class="items-grid">
          <div v-for="quote in quotes" :key="quote.id" class="item-card quote-card">
            <blockquote>{{ quote.quote }}</blockquote>
            <cite>- {{ getCharacterName(quote.character_id) }}</cite>
            <button @click="deleteQuote(quote.id)" class="delete-btn">
              Delete
            </button>
          </div>
        </div>
      </section>
    </main>

    <!-- Loading/Error states -->
    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import api from './services/api.js'

export default {
  name: 'App',
  setup() {
    const characters = ref([])
    const quotes = ref([])
    const loading = ref(false)
    const error = ref('')

    const newCharacter = ref({ name: '' })
    const newQuote = ref({ quote: '', character_id: '' })

    // Computed
    const getCharacterName = computed(() => {
      return (character_id) => {
        const character = characters.value.find(c => c.id === character_id)
        return character ? character.name : 'Unknown'
      }
    })

    // API calls
    const fetchCharacters = async () => {
      try {
        loading.value = true
        const response = await api.get('/characters')
        characters.value = response.data
      } catch (err) {
        error.value = 'Error fetching characters'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const fetchQuotes = async () => {
      try {
        loading.value = true
        const response = await api.get('/quotes')
        quotes.value = response.data
      } catch (err) {
        error.value = 'Error fetching quotes'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const createCharacter = async () => {
      if (!newCharacter.value.name) return

      try {
        loading.value = true
        await api.post('/characters', newCharacter.value)
        newCharacter.value = { name: '' }
        await fetchCharacters()
      } catch (err) {
        error.value = 'Error creating character'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const createQuote = async () => {
      if (!newQuote.value.quote || !newQuote.value.character_id) return

      try {
        loading.value = true
        await api.post('/quotes', newQuote.value)
        newQuote.value = { quote: '', character_id: '' }
        await fetchQuotes()
      } catch (err) {
        error.value = 'Error creating quote'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const deleteCharacter = async (id) => {
      if (!confirm('Are you sure you want to delete this character?')) return

      try {
        loading.value = true
        await api.delete(`/characters/${id}`)
        await fetchCharacters()
        await fetchQuotes() // Refresh quotes in case any were affected
      } catch (err) {
        error.value = 'Error deleting character'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const deleteQuote = async (id) => {
      if (!confirm('Are you sure you want to delete this quote?')) return

      try {
        loading.value = true
        await api.delete(`/quotes/${id}`)
        await fetchQuotes()
      } catch (err) {
        error.value = 'Error deleting quote'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    // Initialize data
    onMounted(async () => {
      await Promise.all([fetchCharacters(), fetchQuotes()])
    })

    return {
      characters,
      quotes,
      loading,
      error,
      newCharacter,
      newQuote,
      getCharacterName,
      createCharacter,
      createQuote,
      deleteCharacter,
      deleteQuote
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  margin-bottom: 40px;
}

h1 {
  color: #333;
  font-size: 2.5em;
}

.section {
  background: white;
  border-radius: 10px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #444;
  margin-bottom: 20px;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

.form-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

input,
textarea,
select {
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  flex: 1;
  min-width: 200px;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #007bff;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.item-card {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quote-card {
  flex-direction: column;
  align-items: flex-start;
}

.quote-card blockquote {
  font-style: italic;
  margin-bottom: 10px;
  line-height: 1.4;
}

.quote-card cite {
  font-weight: bold;
  color: #666;
  margin-bottom: 10px;
}

.delete-btn {
  background-color: #dc3545;
  padding: 8px 12px;
  font-size: 12px;
}

.delete-btn:hover {
  background-color: #c82333;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: #666;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 5px;
  margin: 20px 0;
  border: 1px solid #f5c6cb;
}

@media (max-width: 768px) {
  .form-group {
    flex-direction: column;
  }

  .items-grid {
    grid-template-columns: 1fr;
  }

  .item-card {
    flex-direction: column;
    gap: 10px;
  }
}
</style>