export function getErrorMessage(error, fallback = '请求失败') {
    if (!error) return fallback
  
    const data = error.response?.data
  
    if (typeof data?.message === 'string' && data.message.trim()) {
      return data.message
    }
  
    if (typeof data?.detail === 'string' && data.detail.trim()) {
      return data.detail
    }
  
    if (typeof data?.errors === 'object' && data.errors !== null) {
      try {
        const values = Object.values(data.errors).flat()
        if (values.length > 0) {
          return values.join('；')
        }
        return JSON.stringify(data.errors)
      } catch {
        return fallback
      }
    }
  
    if (typeof error.message === 'string' && error.message.trim()) {
      return error.message
    }
  
    return fallback
  }