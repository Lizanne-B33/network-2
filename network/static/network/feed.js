// Global Variables

document.addEventListener('DOMContentLoaded', function () {
    // By default, load the all posts feed
    load_feed()
})

function load_feed() {
    // variables
    // set views
    show_all_posts_view()
    // Get Posts
    fetch('/api/feed')
        .then(response => response.json())
        .then(posts => {
            // send to format the list
            format_feed(posts, "#all-posts")
        })
}
function load_single_feed(username) {
    // variables
    // Get Posts
    fetch(`/api/single_feed/${username}`)
        .then(response => response.json())
        .then(posts => {
            // send to format the list
            format_feed(posts, "#profile_posts")
        })
}
function format_feed(posts, divStructure) {
    console.log(divStructure)
    startDiv = document.querySelector(divStructure)
    author = ""
    console.log(startDiv)
    id_code = "s_"
    // Update Welcome
    if (divStructure === "#all-posts") {
        document.getElementById("welcome-h").textContent = "Welcome to Our Community"
        document.getElementById("welcome-p").textContent = "Welcome! Feel free to browse our latest posts and explore what our writers have to share. To enjoy the full experience, including personalized features and member-only content, please sign in. You can click on any writer’s name to view their bio, or select a post title to read the full article. We’d love for you to join our group—members can create posts, like content, and connect with others in the community."
        id_code = "a_"
    }
    // loop through each post and render the author and their posts.
    posts.forEach((post) => {
        my_author = post.created_by_id

        if (author != my_author) {
            author = my_author
            // create a div for author
            aDiv = document.createElement('div')
            startDiv.appendChild(aDiv)
            aDiv.setAttribute('id', id_code + my_author)
            aDiv.classList.add('row', 'profile_listener')

            aCDiv = document.createElement('div')
            aDiv.appendChild(aCDiv)
            aCDiv.classList.add('col-12', 'author')

            aHeading = document.createElement('h5')
            aCDiv.appendChild(aHeading)
            s1 = post.created_by
            s2 = s1.charAt(0).toUpperCase() + s1.slice(1);
            aHeading.textContent = s2 + "'s Posts"

            // add listener to view profile
            aDiv.addEventListener('click', function () {
                load_profile(my_author)
            })
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
            colDiv.setAttribute('id', id_code + post.id + '-' + (colIndex + 1))
            colDiv.classList.add(colClass, colStyle, colAlign)
            colDiv.textContent = text
            colDiv.addEventListener('click', function () {
                load_post(post.id)
            })
        })
    })
}
function load_profile(id) {
    // variables

    // Get profile
    fetch(`/api/single_profile/${id}`)
        .then(response => response.json())
        .then(member => {
            // send to format the list
            format_profile(member)
        })
}
function format_profile(member) {
    // hide the posts view & show just single member profile
    show_profile_view()
    // variables
    s1 = member.username
    s2 = s1.charAt(0).toUpperCase() + s1.slice(1);

    // populate the HTML
    document.getElementById("welcome-h").textContent = "Writer Profile"
    document.getElementById("welcome-p").textContent = "This is a public writer profile. Here, you can learn more about the author, explore their bio, and discover the posts they've shared with the community. Feel free to browse and get inspired by their work. To unlock full features like creating posts, liking content, and joining the conversation, consider signing in or becoming a member."

    document.getElementById('profile_img').src = member.profile_pic
    document.getElementById('profile_name').textContent = s2
    document.getElementById('start_date').textContent = "Member since " + member.start_date
    document.getElementById('bio').textContent = member.bio
    document.getElementById('following').textContent = "Followed by: " + member.followers
    document.getElementById('followed_by').textContent = "Following: " + member.following
    load_single_feed(member.username)
}

function load_single_post(id) {
    // variables
    // Get Posts
    fetch(`/api/single_post/${id}`)
        .then(response => response.json())
        .then(posts => {
            // send to format the list
            format_single_post(posts, "#single_posts")
        })
}
function format_single_post(post) {


}

// --------------------------- Helper Functions -------------------------//
function show_all_posts_view() {
    document.querySelector('#all-posts').style.display = 'block'
    document.querySelector('#profile').style.display = 'none'
    document.querySelector('#profile_posts').style.display = 'none'
}

function show_profile_view() {
    document.querySelector('#all-posts').style.display = 'none'
    document.querySelector('#profile_posts').style.display = 'block'
    document.querySelector('#profile').style.display = 'block'
}