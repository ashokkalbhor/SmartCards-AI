# Reddit-Style Community Discussion Module

A comprehensive Reddit-style community discussion system integrated into the SmartCards AI application, allowing users to discuss credit cards, share experiences, and engage in threaded conversations.

## Features

### 🎯 Core Features
- **Posts**: Create, read, update, and delete posts with titles and optional body content
- **Comments**: Nested threaded comments with unlimited depth (limited to 3 levels in UI)
- **Voting**: Upvote/downvote system for both posts and comments
- **Real-time Updates**: Dynamic vote counts and comment counts
- **User Authentication**: Full integration with existing auth system
- **Responsive Design**: Works seamlessly on desktop and mobile

### 📊 Advanced Features
- **Sorting Options**: Sort posts by newest, oldest, or most voted
- **Pagination**: Load more posts with infinite scroll
- **Time Stamps**: "2h ago", "3d ago" format for all timestamps
- **Author Controls**: Edit and delete own posts/comments
- **Soft Deletes**: Posts and comments are soft-deleted to preserve data integrity

## Backend Architecture

### Database Models

#### `CommunityPost`
- `id`: Primary key
- `user_id`: Foreign key to User
- `card_master_id`: Foreign key to CardMasterData
- `title`: Post title (max 300 chars)
- `body`: Optional post content
- `upvotes`, `downvotes`: Vote counters
- `comment_count`: Number of comments
- `is_deleted`: Soft delete flag
- `created_at`, `updated_at`: Timestamps

#### `CommunityComment`
- `id`: Primary key
- `user_id`: Foreign key to User
- `post_id`: Foreign key to CommunityPost
- `parent_id`: Self-referencing for nested comments
- `body`: Comment content
- `upvotes`, `downvotes`: Vote counters
- `is_deleted`: Soft delete flag
- `created_at`, `updated_at`: Timestamps

#### `PostVote` & `CommentVote`
- `id`: Primary key
- `user_id`: Foreign key to User
- `post_id`/`comment_id`: Foreign key to respective entity
- `vote_type`: "upvote" or "downvote"
- `created_at`: Timestamp

### API Endpoints

#### Posts
- `GET /community/cards/{card_id}/posts` - Get posts for a card
- `POST /community/cards/{card_id}/posts` - Create a new post
- `GET /community/posts/{post_id}` - Get detailed post with comments
- `PUT /community/posts/{post_id}` - Update a post
- `DELETE /community/posts/{post_id}` - Delete a post

#### Comments
- `POST /community/posts/{post_id}/comments` - Create a comment
- `PUT /community/comments/{comment_id}` - Update a comment
- `DELETE /community/comments/{comment_id}` - Delete a comment

#### Voting
- `POST /community/posts/{post_id}/vote` - Vote on a post
- `POST /community/comments/{comment_id}/vote` - Vote on a comment

### Query Parameters
- `skip`: Pagination offset
- `limit`: Number of items per page (max 100)
- `sort_by`: "newest", "oldest", or "votes"

## Frontend Components

### Pages
- **CommunityPage**: Main community page showing all posts for a card
- **PostDetailPage**: Detailed view of a single post with all comments

### Components
- **PostCard**: Individual post display with voting and metadata
- **Comment**: Recursive comment component with nested replies
- **TimeUtils**: Utility for formatting timestamps as "time ago"

### Features
- **Infinite Scroll**: Load more posts as user scrolls
- **Real-time Voting**: Instant vote count updates
- **Nested Comments**: Threaded comment display with depth limits
- **Edit/Delete**: Author controls for own content
- **Responsive Design**: Mobile-friendly interface

## Database Migration

The community tables are created via Alembic migration:

```bash
# Run migration
python3 -m alembic upgrade head
```

This creates:
- `community_posts` table
- `community_comments` table  
- `post_votes` table
- `comment_votes` table

## Usage Examples

### Creating a Post
```javascript
const postData = {
  title: "Best rewards for dining",
  body: "I'm looking for a card with good dining rewards..."
};

await communityAPI.createPost(cardId, postData);
```

### Adding a Comment
```javascript
const commentData = {
  body: "Great question! I recommend the HDFC Regalia...",
  parent_id: null // For top-level comment
};

await communityAPI.createComment(postId, commentData);
```

### Voting
```javascript
await communityAPI.voteOnPost(postId, 'upvote');
await communityAPI.voteOnComment(commentId, 'downvote');
```

## Security Features

- **Authentication Required**: All write operations require valid JWT token
- **Authorization**: Users can only edit/delete their own content
- **Input Validation**: All inputs validated with Pydantic schemas
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **Rate Limiting**: Can be easily added with FastAPI middleware

## Performance Optimizations

- **Database Indexes**: Proper indexing on foreign keys and timestamps
- **Pagination**: Efficient pagination with skip/limit
- **Eager Loading**: Comments loaded with posts to reduce queries
- **Caching**: Ready for Redis integration for vote counts

## Future Enhancements

- **Real-time Updates**: WebSocket integration for live updates
- **Rich Text**: Markdown support for posts and comments
- **Media Uploads**: Image and file attachments
- **Moderation**: Admin tools for content moderation
- **Notifications**: Email/notification system for replies
- **Search**: Full-text search for posts and comments
- **Tags**: Categorization system for posts

## Testing

Run the test script to verify functionality:

```bash
cd backend
python3 test_community.py
```

## Integration

The community module is fully integrated into the existing SmartCards AI application:

1. **Navigation**: Access via card detail pages
2. **Authentication**: Uses existing user system
3. **Styling**: Consistent with app theme
4. **Routing**: Integrated into React Router

## API Documentation

Full API documentation available at `/docs` when running the FastAPI server.

## Contributing

When adding new features:
1. Update database models if needed
2. Add API endpoints
3. Create frontend components
4. Update routing
5. Add tests
6. Update documentation 