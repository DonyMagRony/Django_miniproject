async function apiFetch(url, options = {}) {
    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNzY3Nzk0LCJpYXQiOjE3NDA2ODEzOTQsImp0aSI6IjQxNzU5MDEzNmZkYjRlMjI9YzYwZjFhYTAxMzIyMTk0IiwidXNlcl9pZCI6MX0.AqEwJQiS4AssLlWa40p2md_u27eBWum9QUcy2ECnZgc"
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
    };

    try {
        const response = await fetch(url, { ...options, headers });

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = '/login/';
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}