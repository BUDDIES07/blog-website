document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('searchBar');
    searchBar.addEventListener('input', searchPosts);

    async function fetchPosts() {
        try {
            const response = await fetch('/posts');
            const posts = await response.json();
            return posts;
        } catch (error) {
            console.error('Error fetching posts:', error);
            return [];
        }
    }

    async function searchPosts() {
        const query = searchBar.value.toLowerCase();
        const posts = await fetchPosts();
        const filteredPosts = posts.filter(post =>
            post.title.toLowerCase().includes(query) ||
            (post.content && post.content.toLowerCase().includes(query))
        );

        displayPosts(filteredPosts);
    }

    function displayPosts(posts) {
        const postContainer = document.getElementById('postContainer');
        postContainer.innerHTML = ''; // Clear existing content

        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post';
            postElement.innerHTML = `
                ${post.image ? `<img src="${post.image}" alt="Post Image">` : ''}
                <h3>${post.title}</h3>
                <p><strong>Author:</strong> ${post.author}</p>
                <p>${post.content}</p>
            `;
            postContainer.appendChild(postElement);
        });
    }

    // Initial display of posts
    searchPosts();
});
