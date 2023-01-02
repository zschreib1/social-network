# social-network
**I designed a Twitter-like social network website for making posts and following users**, using **Django**, **Python**, **JavaScript**, **HTML**, **CSS**, **Bootstrap**.

Starter code was provided for this project, which I completed in the context of Harvard UniversityX's [CS50 Introduction to Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/) course.

View a short [video demo](https://www.youtube.com/watch?v=tSlvI1tTz4Q) of the project.

## Implementation
I completed the implementation of a social network that allows users to **make posts**, **follow other users**, and **“like” posts**. 

**Requirements:**

- *New Post*: Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
  <sub>The screenshot at the top of this specification shows the “New Post” box at the top of the “All Posts” page. You may choose to do this as well, or you may make the “New Post” feature a separate page.</sub>
- *All Posts*: The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.
  <sub>Each post should include the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has (this will be 0 for all posts until you implement the ability to “like” a post later).</sub>
- *Profile Page*: Clicking on a username should load that user’s profile page. 
  <sub>Display the number of followers the user has, as well as the number of people that the user follows.</sub>
  <sub>Display all of the posts for that user, in reverse chronological order.</sub>
  <sub>For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.</sub>
- *Following*: The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.
- *Pagination*: On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.
- *Edit Post*: Users should be able to click an “Edit” button or link on any of their own posts to edit that post.
- *“Like” and “Unlike”*: Users should be able to click a button or link on any post to toggle whether or not they “like” that post.

Visit the [Harvard CS50W](https://cs50.harvard.edu/web/2020/projects/4/network/) website for more information about the requirements for the project. Please do **not** directly use the source code as it is **only** for reference. Plagiarism is strictly prohibited by both Harvard University and the edX platform. See academic honesty for details.
