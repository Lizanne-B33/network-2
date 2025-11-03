// Global Variables

document.addEventListener('DOMContentLoaded', function () {
    // By default, load the all posts feed
    load_feed()
})

function load_feed() {
    // variables

    // Get Posts
    fetch('/api/feed')
        .then(response => response.json())
        .then(posts => {
            // send to format the list
            format_feed(posts)
            console.log(posts)
        })
}

function format_feed(posts) {
    const startDiv = document.querySelector("#all-posts")
    author = ""

    // loop through each post and render the author and their posts.
    posts.forEach((post) => {
        my_author = post.created_by_id
        console.log(my_author)
        console.log(author)

        if (author != my_author) {
            author = my_author
            // create a div for author
            aDiv = document.createElement('div')
            startDiv.appendChild(aDiv)
            aDiv.setAttribute('id', my_author)
            aDiv.classList.add('row')

            aCDiv = document.createElement('div')
            aDiv.appendChild(aCDiv)
            aDiv.classList.add('column', 'author')

            aHeading = document.createElement('h5')
            aCDiv.appendChild(aHeading)
            s1 = post.created_by
            s2 = s1.charAt(0).toUpperCase() + s1.slice(1);
            aHeading.textContent = s2 + "'s Posts"

            //To Do
            //rowDiv.addEventListener('click', function () {
            //    load_profile(my_author)})
        }

        // create div for the posts
        pDiv = document.createElement('div')
        startDiv.appendChild(pDiv)
        pDiv.classList.add('row', 'postsRow')

        // Show the title, time stamp and likes 
        columns = [6, 3, 3]
        columns.forEach((column, colIndex) => {
            // Variables
            colClass = 'col-' + column
            switch (colIndex) {
                case 0:
                    text = post.title
                    colStyle = 'colTitle'
                    colAlign = 'text-left'
                    break
                case 1:
                    text = post.create_date
                    colStyle = 'colDate'
                    colAlign = 'text-left'
                    break
                case 2:
                    text = String.fromCodePoint(0x2764) + " " + post.likes
                    colStyle = 'colTimestamp'
                    colAlign = 'text-right'
            }
            // build the columns
            colDiv = document.createElement('div')
            pDiv.appendChild(colDiv)
            colDiv.setAttribute('id', post.id + '-' + (colIndex + 1))
            colDiv.classList.add(colClass, colStyle, colAlign)
            colDiv.textContent = text
            colDiv.addEventListener('click', function () {
                load_post(post.id)
            })
        })
    })
}
