[![](https://dev.are.na/assets/arena-mark-a778d5c8fca2b357f25a704124ac568d2c22bc994936c857623d61ac17596e91.svg) Developer](https://dev.are.na/)

![](https://s3.amazonaws.com/arena-avatars/12768/large_f9f88cb62a16e409856309fd157c55fa.png)

[Your applications](https://dev.are.na/oauth/applications) [Applications you’ve authorized](https://dev.are.na/oauth/authorized_applications) [Logout](https://dev.are.na/users/sign_out)

[Resources](https://dev.are.na/resources) [API V2](https://dev.are.na/documentation/channels)

[Authentication](https://dev.are.na/documentation/authentication) [Channels](https://dev.are.na/documentation/channels) [Blocks](https://dev.are.na/documentation/blocks) [Users](https://dev.are.na/documentation/users) [Search](https://dev.are.na/documentation/search)

## Channels

[Introduction](https://dev.are.na/documentation/channels#Block52055)[Attributes](https://dev.are.na/documentation/channels#Block52095)[Block attributes](https://dev.are.na/documentation/channels#Block52096)[GET /v2/channels](https://dev.are.na/documentation/channels#Block43473)[GET /v2/channels/:slug](https://dev.are.na/documentation/channels#Block43472)[GET /v2/channels/:slug/thumb](https://dev.are.na/documentation/channels#Block43474)[GET /v2/channels/:id/connections](https://dev.are.na/documentation/channels#Block45050)[GET /v2/channels/:id/connections](https://dev.are.na/documentation/channels#Block45053)[GET /v2/channels/:id/contents](https://dev.are.na/documentation/channels#Block45052)[POST /v2/channels](https://dev.are.na/documentation/channels#Block45041)[PUT /v2/channels/:slug](https://dev.are.na/documentation/channels#Block45048)[PUT /v2/channels/:slug/sort](https://dev.are.na/documentation/channels#Block45054)[DELETE /v2/channels/:slug](https://dev.are.na/documentation/channels#Block45049)[POST /v2/channels/:slug/blocks](https://dev.are.na/documentation/channels#Block45059)[GET /v2/channels/:id/collaborators](https://dev.are.na/documentation/channels#Block59794)[POST /v2/channels/:id/collaborators](https://dev.are.na/documentation/channels#Block59795)[DELETE /v2/channels/:id/collaborators](https://dev.are.na/documentation/channels#Block59796)

### Introduction

Channels are organizational structures for content. This means *blocks* but also sometimes other *channels*. Channels have a primary *user* (indicated by the user*id) but can also have _collaborators* (an array of *users*). Channels can be public (anyone can view and add), closed (only the channel's author and collaborators can add but everyone can view) and private (only the channels authors and collaborators can view and add).

See also: [What is a channel?](http://are.na/faq/show:6767)

### Attributes

|                    |                      |                                                                                                                                                                                                                                                                               |
| ------------------ | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **id**             | (Integer)            | The internal ID of the channel                                                                                                                                                                                                                                                |
| **title**          | (String)             | The title of the channel                                                                                                                                                                                                                                                      |
| **created_at**     | (Timestamp)          | Timestamp when the channel was created                                                                                                                                                                                                                                        |
| **updated_at**     | (Timestamp)          | Timestamp when the channel was last updated                                                                                                                                                                                                                                   |
| **published**      | (Boolean)            | If channel is visible to all members of arena or not                                                                                                                                                                                                                          |
| **open**           | (Boolean)            | If channel is open to other members of arena for adding blocks                                                                                                                                                                                                                |
| **collaboration**  | (Boolean)            | If the channel has collaborators or not                                                                                                                                                                                                                                       |
| **slug**           | (String)             | The slug of the channel used in the url (e.g. http://are.na/arena-influences)                                                                                                                                                                                                 |
| **length**         | (Integer)            | The number of items in a channel (blocks and other channels)                                                                                                                                                                                                                  |
| **kind**           | (String)             | Can be either "default" (a standard channel) or "profile" the default channel of a user                                                                                                                                                                                       |
| **status**         | (String)             | Can be "private" (only open for reading and adding to the channel by channel author and collaborators), "closed" (open for reading by everyone, only channel author and collaborators can add) or "public" (everyone can read and add to the channel)                         |
| **user_id**        | (Integer)            | Internal ID of the channel author                                                                                                                                                                                                                                             |
| **class**          | (String)             | Will always be "Channel"                                                                                                                                                                                                                                                      |
| **base_class**     | (String)             | Will always be "Channel"                                                                                                                                                                                                                                                      |
| **user**           | (Hash)               | More information on the channel author. Contains *id*, *slug*, *first_name*, *last_name*, *full_name*, *avatar*, *email*, *channel_count*, *following_count*, *follower_count*, and *profile_id*                                                                              |
| **total_pages**    | (Integer)            | If pagination is used, how many total pages there are in your request                                                                                                                                                                                                         |
| **current_page**   | (Integer)            | If pagination is used, page requested                                                                                                                                                                                                                                         |
| **per**            | (Integer)            | If pagination is used, items per page requested                                                                                                                                                                                                                               |
| **follower_count** | (Integer)            | Number of followers the channel has                                                                                                                                                                                                                                           |
| **contents**       | (Array, can be null) | Array of blocks and other channels in the channel. **Note:** If the request is authenticated, this will include any private channels included in the requested channel that you have access to. If not, only public channels included in the requested channel will be shown. |
| **collaborators**  | (Array, can be null) | Collaborators on the channel                                                                                                                                                                                                                                                  |

### Block attributes

Blocks inside the channel's contents node have attributes that are specific to the channel:

|                          |             |                                                                                                                                                                                      |
| ------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **position**             | (Integer)   | The position of the block inside the channel (as determined by the channel's author and collaborators)                                                                               |
| **selected**             | (Boolean)   | Block is marked as selected inside the channel (this is an initial attempt to allow users to "feature" some content over others, can be used for moderation, introduction text, etc) |
| **connected_at**         | (Timestamp) | Time when block was connected to the channel (if the block was created at the same time as the channel this will be identical to *created_at*)                                       |
| **connected_by_user_id** | (Integer)   | ID of the user who connected the block to the channel (if the block was not reused by another user, this will be identical to *user_id*)                                             |

### GET /v2/channels

**Resource URL:**  
[http://api.are.na/v2/channels](http://api.are.na/v2/channels)

**Example Request:**  
`GET [http://api.are.na/v2/channels?page=2&amp;per=15](http://api.are.na/v2/channels?page=2&per=15)`

_Returns a list of **published** channels._

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### GET /v2/channels/:slug

**Resource URL:**  
[http://api.are.na/v2/channels/:slug](http://api.are.na/v2/channels/:slug)

**Example Request:**  
`GET [http://api.are.na/v2/channels/faq](http://api.are.na/v2/channels/faq)`

_Returns a complete representation of a channel. Channel contents can be paginated._

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### GET /v2/channels/:slug/thumb

**Resource URL:**  
[http://api.are.na/v2/channels/:slug/thumb](http://api.are.na/v2/channels/:slug/thumb)

**Example Request:**  
`GET [http://api.are.na/v2/channels/arena-influences/thumb](http://api.are.na/v2/channels/arena-influences/thumb)`

_Returns some fixed basic information for constructing a small channel representation. For now: returns the first 9 blocks of the channel. This may change._

---

HTTP method: GET  
Pagination: No  
Requires authentication: No

### GET /v2/channels/:id/connections

**Resource URL:**  
[http://api.are.na/v2/channels/:id/connections](http://api.are.na/v2/channels/:id/connections)

**Example Request:**  
`GET [http://api.are.na/v2/channels/arena-influences/connections](http://api.are.na/v2/channels/arena-influences/connections)`

_Returns all the connections within a channel without fetching actual objects._

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### GET /v2/channels/:id/connections

**Resource URL:**  
[http://api.are.na/v2/channels/:id/channels](http://api.are.na/v2/channels/:id/channels)

**Example Request:**  
`GET [http://api.are.na/v2/channels/arena-influences/channels](http://api.are.na/v2/channels/arena-influences/channels)`

_Returns **all** of the channels connected to blocks in the channel. For instance if one wanted to spider the connections between channels_

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### GET /v2/channels/:id/contents

**Resource URL:**  
[http://api.are.na/v2/channels/:id/contents](http://api.are.na/v2/channels/:id/contents)

**Example Request:**  
`GET [http://api.are.na/v2/channels/arena-influences/contents](http://api.are.na/v2/channels/arena-influences/contents)`

_Returns all the contents of a channel. Nothing else (collaborators, etc.)_

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### POST /v2/channels

**Resource URL:**  
[http://api.are.na/v2/channels](http://api.are.na/v2/channels)

**Parameters:**  
*:title* (required)  
Title of the channel

*:status* (optional)  
Sets the visibility of the channel. Can be: ["public", "closed", "private"]  
Defaults to "public"

_Creates a new channel_

---

HTTP Method: POST  
Requires authentication: Yes

### PUT /v2/channels/:slug

**Resource URL:**  
[http://api.are.na/v2/channels/:slug](http://api.are.na/v2/channels/:slug)

**Parameters:**  
*:title* (optional)  
Title of the channel

*:status* (optional)  
Sets the visibility of the channel. Can be: ["public", "closed", "private"]  
Defaults to "public"

_Updates the channels attributes_

---

HTTP Method: PUT  
Requires authentication: Yes

### PUT /v2/channels/:slug/sort

**Resource URL:**  
[http://api.are.na/v2/channels/:slug/sort](http://api.are.na/v2/channels/:slug/sort)

**Parameters:**  
*:ids* (required)  
Serialized array of IDs

_Accepts a serialized array of IDs. Updates the order of the channel to the order of the IDs._

---

HTTP method: PUT  
Requires authentication: Yes

### DELETE /v2/channels/:slug

**Resource URL:**  
[http://api.are.na/v2/channels/:slug](http://api.are.na/v2/channels/:slug)

_Destroys the channel and connections to content. Content contained within is not destroyed._

---

HTTP method: DELETE  
Requires authentication: Yes

### POST /v2/channels/:slug/blocks

**Resource URL:**  
[http://api.are.na/v2/channels/:slug/blocks](http://api.are.na/v2/channels/:slug/blocks)

**Parameters:**  
*:source* (required\*)  
URL of content. Can be an Image, Embed, or Link.

*:content* (required\*)  
Textual content that's rendered with Github Flavored Markdown.

*Either \*:source* or *:content* is required. Not both.

_Creates a new block and adds it to the specified channel._

---

HTTP method: POST  
Requires authentication: Yes

### GET /v2/channels/:id/collaborators

**Resource URL:**  
[http://api.are.na/v2/channels/:slug/collaborators](http://api.are.na/v2/channels/:slug/collaborators)

**Example Request:**  
`GET [http://api.are.na/v2/channels/arena-influences/collaborators](http://api.are.na/v2/channels/arena-influences/collaborators)`

_Returns all members that are part of a channel. Does not return channel owner_

---

HTTP method: GET  
Requires authentication: No

### POST /v2/channels/:id/collaborators

**Resource URL:**  
[http://api.are.na/v2/channels/:slug/collaborators](http://api.are.na/v2/channels/:slug/collaborators)

**Example Request:**  
`POST [http://api.are.na/v2/channels/arena-influences/collaborators](http://api.are.na/v2/channels/arena-influences/collaborators)`

_Accepts a serialized list of ids. Returns the current list of collaborators_

---

HTTP method: POST  
Requires authentication: Yes

### DELETE /v2/channels/:id/collaborators

**Resource URL:**  
[http://api.are.na/v2/channels/:slug/collaborators](http://api.are.na/v2/channels/:slug/collaborators)

**Example Request:**  
`DELETE [http://api.are.na/v2/channels/arena-influences/collaborators](http://api.are.na/v2/channels/arena-influences/collaborators)`

_Accepts a serialized list of ids. Include only the ids you want to keep in the channel, excluding the ones you want to delete. Returns the current list of collaborators_

---

HTTP method: DELETE  
Requires authentication: Yes

[![](https://dev.are.na/assets/arena-mark-a778d5c8fca2b357f25a704124ac568d2c22bc994936c857623d61ac17596e91.svg) Developer](https://dev.are.na/)

![](https://s3.amazonaws.com/arena-avatars/12768/large_f9f88cb62a16e409856309fd157c55fa.png)

[Your applications](https://dev.are.na/oauth/applications) [Applications you’ve authorized](https://dev.are.na/oauth/authorized_applications) [Logout](https://dev.are.na/users/sign_out)

[Resources](https://dev.are.na/resources) [API V2](https://dev.are.na/documentation/channels)

[Authentication](https://dev.are.na/documentation/authentication) [Channels](https://dev.are.na/documentation/channels) [Blocks](https://dev.are.na/documentation/blocks) [Users](https://dev.are.na/documentation/users) [Search](https://dev.are.na/documentation/search)

## Blocks

[Introduction](https://dev.are.na/documentation/blocks#Block52054)[Attributes](https://dev.are.na/documentation/blocks#Block52094)[GET /v2/blocks/:id](https://dev.are.na/documentation/blocks#Block45056)[GET /v2/blocks/:id/channels](https://dev.are.na/documentation/blocks#Block45058)[POST /v2/channels/:slug/blocks](https://dev.are.na/documentation/blocks#Block45059)[PUT /v2/blocks/:id](https://dev.are.na/documentation/blocks#Block45082)[DELETE /v2/channel/:channel_id/blocks/:id](https://dev.are.na/documentation/blocks#Block45240)

### Introduction

Blocks are modular and reusable pieces of data or content. A block has primary user (indicated by user*id) and can only be edited by the user who created it. However, any block can be reused in multiple channels (this is called a _connection*). The channels a block appears in across Arena are listed in the blocks' *connections* attribute.

These connections are shown depending on the authenticated users access. For example, if a block appears in 5 public channels and 2 private channels, an unauthenticated request will display only the public channels a block appears in, but an authenticated request will show the public channels as well as the private channels that the authenticated user has access to.

Blocks can also take many forms: a text, a link (a captioned link to an external website, with a screenshot), an embed (embeddable media such as a YouTube or Vimeo video), an image (either uploaded from a users' computer or saved from an external website), or an attachment (a file uploaded from a users' computer or from an external website, see also: [What file types can I upload to Arena?](http://are.na/faq/show:49941)).

### Attributes

|                      |                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **id**               | (Integer)             | The internal ID of the block                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **title**            | (String, can be null) | The title of the block                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **updated_at**       | (Timestamp)           | Timestamp when the block was last updated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **created_at**       | (Timestamp)           | Timestamp when the block was created                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **state**            | (String)              | Represents the state of the blocks processing lifecycle (this will most often "Available" but can also be "Failure", "Processed", "Processing")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **comment_count**    | (Integer)             | The number of comments on a block                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **generated_title**  | (String)              | If the title is present on the block, this will be identical to the title. Otherwise it will be a truncated string of the _description_ or _content_. If neither of those are present, it will be "Untitled"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **class**            | (String)              | The type of block. Can be "Image", "Text", "Link", "Media", or "Attachment"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **base_class**       | (String)              | This will always be "Block"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **content**          | (String, can be null) | If the block is of class "Text", this will be the text content as markdown                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **content_html**     | (String, can be null) | If the block is of class "Text", this will be the text content as HTML                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **description**      | (String, can be null) | This is used for captioning any type of block. Returns markdown.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **description_html** | (String, can be null) | This is used for captioning any type of block. Returns HTML                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **source**           | (Hash, can be null)   | If the Block is saved from somewhere on the web, this returns a Hash representation of the source <br> <br><br>\| \| \| \|<br>\|---\|---\|---\|<br>\|**url**\|(String)\|The url of the source\|<br>\|**provider**\|(Hash)\|A hash of more info about the provider **name**: (String) The name of the source provider **url**: (String) The hostname of the source provider\|<br><br>`<br></td><br>`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **image**            | (Hash, can be null)   | If the Block is of class "Image" or "Link", this will be a Hash representation of the various sizes of images that Arena provides (in the case of a "Link" it will be a screenshot of the website). <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br><br>\| \| \| \|<br>\|---\|---\|---\|<br>\|**filename**\|(String)\|Name of the file as it appears on the Arena filesystem\|<br>\|**content_type**\|(String)\|MIME type of the image (e.g. 'image/png')\|<br>\|**updated_at**\|(Timestamp)\|Timestamp of the last time the file was updated\|<br>\|**thumb**\|(Hash)\|Only contains *url* which is a URL of the thumbnail sized image (200x200)\|<br>\|**display**\|(Hash)\|Only contains *url* which is a URL of the display sized image (same aspect ratio as original image but with a maximim width of 600px or a maximum height of 600px, whichever comes first)\|<br>\|**original**\|(Hash)\|Contains *url* which is a URL of the original image as well *file_size* (an integer representation in bytes) and *file_size_display* (a nicer string representation of the file_size)\| |
| **user**             | (Hash)                | Representation of the author of the block                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **connections**      | (Array)               | An array of hash representations of each of the channels the block appears in                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

### GET /v2/blocks/:id

**Resource URL:**  
[http://api.are.na/v2/blocks/:id](http://api.are.na/v2/blocks/:id)

**Example Request:**  
`GET [http://api.are.na/v2/blocks/8693](http://api.are.na/v2/blocks/8693)`

_Returns the full representation of a block_

---

HTTP method: GET  
Requires authentication: No

### GET /v2/blocks/:id/channels

**Resource URL:**  
[http://api.are.na/v2/blocks/:id/channels](http://api.are.na/v2/blocks/:id/channels)

**Example Request:**  
`GET [http://api.are.na/v2/blocks/8693/channels](http://api.are.na/v2/blocks/8693/channels)`

_Returns a paginated list of channels the block exists in_

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### POST /v2/channels/:slug/blocks

**Resource URL:**  
[http://api.are.na/v2/channels/:slug/blocks](http://api.are.na/v2/channels/:slug/blocks)

**Parameters:**  
*:source* (required\*)  
URL of content. Can be an Image, Embed, or Link.

*:content* (required\*)  
Textual content that's rendered with Github Flavored Markdown.

*Either \*:source* or *:content* is required. Not both.

_Creates a new block and adds it to the specified channel._

---

HTTP method: POST  
Requires authentication: Yes

### PUT /v2/blocks/:id

**Resource URL:**  
[http://api.are.na/v2/blocks/:id](http://api.are.na/v2/blocks/:id)

**Parameters:**  
*:title* (optional)

*:description* (optional)  
Markdown formatted text.

*:content* (optional)  
Markdown formatted text. For text block type only.

_Updates a block's attributes_

---

HTTP method: PUT  
Requires authentication: No

### DELETE /v2/channel/:channel_id/blocks/:id

**Resource URL:**  
[http://api.are.na/v2/channel/:slug/blocks/:id](http://api.are.na/v2/channel/:slug/blocks/:id)

Removes a block from the channel it's in (Destroys the connection).

---

HTTP method: DELETE  
Requires authentication: yes

[![](https://dev.are.na/assets/arena-mark-a778d5c8fca2b357f25a704124ac568d2c22bc994936c857623d61ac17596e91.svg) Developer](https://dev.are.na/)

![](https://s3.amazonaws.com/arena-avatars/12768/large_f9f88cb62a16e409856309fd157c55fa.png)

[Your applications](https://dev.are.na/oauth/applications) [Applications you’ve authorized](https://dev.are.na/oauth/authorized_applications) [Logout](https://dev.are.na/users/sign_out)

[Resources](https://dev.are.na/resources) [API V2](https://dev.are.na/documentation/channels)

[Authentication](https://dev.are.na/documentation/authentication) [Channels](https://dev.are.na/documentation/channels) [Blocks](https://dev.are.na/documentation/blocks) [Users](https://dev.are.na/documentation/users) [Search](https://dev.are.na/documentation/search)

## Search

[Introduction](https://dev.are.na/documentation/search#Block59797)[Attributes](https://dev.are.na/documentation/search#Block59798)[GET /v2/search?q=:q](https://dev.are.na/documentation/search#Block59799)[GET /v2/search/users?q=:q](https://dev.are.na/documentation/search#Block59800)[GET /v2/search/channels?q=:q](https://dev.are.na/documentation/search#Block59801)[GET /v2/search/blocks?q=:q](https://dev.are.na/documentation/search#Block59802)

### Introduction

Through these endpoints, you can query the entire system and retrieve *blocks*, *users*, and *channels* whose search index matches your query.

### Attributes

|                  |           |                                                                       |
| ---------------- | --------- | --------------------------------------------------------------------- |
| **term**         | (String)  | A string representation of your search query                          |
| **users**        | (Array)   | An array of the users that match your search query                    |
| **channels**     | (Array)   | An array of the channels that match your search query                 |
| **blocks**       | (Array)   | An array of the blocks that match your search query                   |
| **total_pages**  | (Integer) | If pagination is used, how many total pages there are in your request |
| **current_page** | (Integer) | If pagination is used, page requested                                 |
| **per**          | (Integer) | If pagination is used, items per page requested                       |

### GET /v2/search?q=:q

**Resource URL:**  
[http://api.are.na/v2/search?q=:query](http://api.are.na/v2/search?q=:query)

**Example Request:**  
`GET [http://api.are.na/v2/search?q=art](http://api.are.na/v2/search?q=art)`

_Performs a search_

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### GET /v2/search/users?q=:q

**Resource URL:**  
[http://api.are.na/v2/search/users?q=:query](http://api.are.na/v2/search/users?q=:query)

**Example Request:**  
`GET [http://api.are.na/v2/search/users?q=dan](http://api.are.na/v2/search/users?q=dan)`

_Performs a search_

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### GET /v2/search/channels?q=:q

**Resource URL:**  
[http://api.are.na/v2/search/channels?q=:query](http://api.are.na/v2/search/channels?q=:query)

**Example Request:**  
`GET [http://api.are.na/v2/search/channels?q=arena](http://api.are.na/v2/search/channels?q=arena)`

_Performs a search_

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No

### GET /v2/search/blocks?q=:q

**Resource URL:**  
[http://api.are.na/v2/search/blocks?q=:query](http://api.are.na/v2/search/blocks?q=:query)

**Example Request:**  
`GET [http://api.are.na/v2/search/blocks?q=painting](http://api.are.na/v2/search/blocks?q=painting)`

_Performs a search_

---

HTTP method: GET  
Pagination: Yes  
Requires authentication: No
