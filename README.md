# InstagramReplica

This application is a simplified replica of Instagram, a system where users can create posts. All posts
must have an image attached to it (PNG or JPG only) and a caption. Users can follow each other to see
their posts. Eventually this will lead to a timeline where the posts of a user
and the posts of users they follow will be merged together. Users will also be
permitted to comment on their own or other posts. The Blobstore will solely be used
for managing your images, whereas the Datastore will be used to manage all other information.

Bracket 1
- Write the shell of an application that has a working login/logout
service.
- Create models of a user and posts using appropriate datatypes.
    * If a user logs in for the first time, a user model should be created
      for them.
    * Each user should have a following (people who they are following)
      and a followers list (people who follow them)
