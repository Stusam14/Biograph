import { ref } from 'vue'
export const uploadFiles = async (files: File[]) => {
  const formData = new FormData()

  files.forEach((file) => {
    formData.append('sbml_files', file)
  })

  try {
    const response = await fetch('http://localhost:8000/process-sbmls', {
      method: 'POST',
      body: formData,
      headers: {
        accept: 'application/json' // Only keep the accept header
      }
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(`HTTP error! status ${response.status}, message: ${errorData.message}`)
    }

    const result = await response.json()
    console.log('Upload Success', result)
  } catch (error) {
    if (error instanceof Error) console.error('Upload failed', error.message)
    else {
      console.error('Upload failed', error)
    }
    throw error
  }
}

export const useFetch = (url: string) => {
  interface Data {
    name: string
    community: number
  }
  const data = ref<Data[]>([])
  const error = ref(null)
  fetch(url)
    .then((res) => res.json())
    .then((json) => (data.value = json))
    .catch((err) => (error.value = err))

  return { data, error }
}
