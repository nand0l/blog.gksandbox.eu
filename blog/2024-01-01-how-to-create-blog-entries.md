---
slug: how-to-create-blog-entries
title: How to Create New Blog Entries
authors: [nlu]
tags: [docusaurus, howto]
---

This post explains how to add new articles to this blog. All blog posts live in the `/blog` folder of the repository.

<!-- truncate -->

## File naming

Every blog post is a Markdown (`.md`) or MDX (`.mdx`) file. The filename determines the publication date and URL slug:

```
YYYY-MM-DD-your-post-title.md
```

Example:

```
2024-06-15-my-new-post.md
```

## Front matter

Every post starts with a front matter block between `---` delimiters:

```md
---
slug: my-new-post
title: My New Post
authors: [nlu]
tags: [aws, cloud]
---
```

| Field | Required | Description |
|---|---|---|
| `slug` | No | URL path — defaults to the filename |
| `title` | Yes | Title shown in the blog listing |
| `authors` | Yes | Must match a key in `blog/authors.yml` |
| `tags` | No | List of tags for filtering |

## Truncate marker

The blog listing page shows a preview of each post. Add the truncate marker where you want the preview to end:

```md
This intro paragraph is shown in the listing.

<!-- truncate -->

Everything below this line is only shown on the full post page.
```

## Adding images

Place images in the `/static/img/` folder and reference them like this:

```md
![Alt text](/img/my-image.png)
```

## MDX and React components

If you rename your file to `.mdx` you can use React components inline:

```mdx
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="aws" label="AWS">AWS content here</TabItem>
  <TabItem value="azure" label="Azure">Azure content here</TabItem>
</Tabs>
```

## Publishing

Commit and push the new file to the `main` branch. AWS Amplify picks it up automatically and rebuilds the site.

```powershell
git add blog/2024-06-15-my-new-post.md
git commit -m "Add blog post: My New Post"
git push
```
