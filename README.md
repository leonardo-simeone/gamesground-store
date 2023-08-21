# GAMESGROUND STORE

GamesGround Store, is an ecommerce site designed to provide video games users of a place where they can find information about video games, purchase them and provide feedback about games should they want to. What makes GamesGround Store special is the fact that this store is all about games, nothing else. Nowadays it is common to find thousands of ecommerce stores that sell video games but most of them offer video games and a plethora of other products more, in GamesGround we focus on games.

We give our users a place where they can look for video games and find information about them such as cool synopsis, games trailer videos, PEGI ratings, and of course competitive price. Our user can create their own profiles and save their information securely in our database for future transactions or they can simply purchase their games as guest users.

Users can also subscribe to our newsletter to avail of special offers, news and much more. External links to potential interesting site for users are also included such as gaming accessories shops, gaming news and reviews blogs and blogs about tips and tricks for games.

Store owners/admins can administer the site from the user interface, they have the option to add, edit and delete games as well as have access to the recieved messages and their corresponding information in the contact us section.

![screenshot](documentation/am-i-responsive.png)

## UX

### Colour Scheme

* To select the colors, I used the [ColorSpace](https://mycolor.space/) website which provides the option to input any color you want and then it will provide a selection of matching/compatible colors that relate well to that "base" color you selected in the first place.
* Once I had my base color selected which is [#000000](https://mycolor.space/?hex=%23000000&sub=1), I used ColorSpace and it gave me a wide variety of compatible colors to work with from which I chose several of them and referenced them accordingly in the css style sheet.   

![Colors](documentation/color-selection.png)

### Typography

* Since the google fonts page feature for fonts pairing suggestions was discontinued, I used an alternative tool available to select the fonts for the site.
* I browsed [heyreliable](https://heyreliable.com/ultimate-google-font-pairings/) google fonts pairings available in their collection and selected number 35 based on the look and mood wanted for the site.
    
![Fonts](documentation/fonts-selection.png)

* These fonts are clear to read, they have a friendly yet professional style which is compatible with a video games store website.

- [Catamaran](https://fonts.google.com/specimen/Catamaran) was used for the primary headers and titles.

- [Merriweather Sans](https://fonts.google.com/specimen/Merriweather+Sans) was used for all other secondary text.

- [Font Awesome](https://fontawesome.com) icons were used throughout the site, such as the social media icons in the footer, contact link, newsletter link, among others.

## User Stories

### Site Users

- As a Site User I would like to register for an account so that I can login and out with personal account and recover my password in case I forget it, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/1).
- As a Site User I would like to view a list of games so that I can select one or more to purchase, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/6).
- As a Site User I would like to view an individual game so that I can identify its name, price, image, genre, description, year, platform, pegi rating, trailer video and likes count, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/7).
- As a Site User I would like to search for a specific game name or genre so that I can easily find the game I want to purchase, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/8).
- As a Site User I would like to sort games by price, genre, name, pegi rating and popularity so that I can easily find the games according to my preferences, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/9).
- As a Site User I would like to add, view, update and delete games in the shopping basket so that I can manage/review my shopping basket before proceeding to checkout, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/10).
- As a Site User I would like to easily view the total amount of games in my shopping basket so that I can know how many games are there in my basket at all times, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/11).
- As a Site User I would like to provide the necessary billing/delivery details so that I can purchase games and view an order confirmation after checkout to verify all the information from my purchase is accurate, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/12).
- As a Site User I would like to receive an email confirmation after my purchase so that I can keep records of my transactions, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/13).
- As a Site User I would like to create/manage my personal account profile so that I can view/update my profile, view my order history and save my payment information, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/14).
- As a Site User I would like to contact the site administrator so that I can query/recommend the site admin on different topics, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/16).
- As a Site User I would like to subscribe to a newsletter so that I can receive news, special offers and general information related to the store, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/17).
- As a Site User I would like to navigate to the site's about us, terms & conditions and privacy policy links so that I can inform myself in more depth about the site, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/19).

### Site Admin

- As a site administrator, I should be able to create/add, read, update and delete games so that I can manage the games on the site, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/2).
- As a site administrator, I should be able to add, update and delete pegi ratings so that I can assign pegi ratings to games, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/4).
- As a site administrator, I should be able to add, update and delete platforms so that I can assign platforms to games, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/5).
- As a site administrator/site owner, I should be able to add/edit/delete games from the website so that I can manage new games, games updates or games that are no longer available, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/15).

### Product Owner

- As a product owner, I should be able to run automated tests, so that I can make sure everything is working as it should, [Link here](https://github.com/leonardo-simeone/gamesground-store/issues/18)

## Wireframes

To wireframe the website I used [Whimsical](https://whimsical.com/wireframes).

### Pages Wireframes

| Page | Screenshot |
| --- | --- |
| All pages | ![screenshot](documentation/wireframe-all.png) |
| Home | ![screenshot](documentation/wireframe-home.png) |
| Games | ![screenshot](documentation/wireframe-games.png) |
| Game detail | ![screenshot](documentation/wireframe-game-detail.png) |
| Login/Register | ![screenshot](documentation/wireframe-login-register.png) |
| About us | ![screenshot](documentation/wireframe-about-us.png) |
| Add game | ![screenshot](documentation/wireframe-add-game.png) |
| Edit game | ![screenshot](documentation/wireframe-edit-game.png) |
| Basket | ![screenshot](documentation/wireframe-basket.png) |
| Checkout | ![screenshot](documentation/wireframe-checkout.png) |
| Checkout success | ![screenshot](documentation/wireframe-checkout-success.png) |
| Contact/Newsletter | ![screenshot](documentation/wireframe-contact-newsletter.png) |

This is the Code Institute student template for Gitpod. We have preinstalled all of the tools you need to get started. It's perfectly ok to use this template as the basis for your project submissions.

You can safely delete this README.md file, or change it for your own project. Please do read it at least once, though! It contains some important information about Gitpod and the extensions we use. Some of this information has been updated since the video content was created. The last update to this file was: **September 1, 2021**

## Gitpod Reminders

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

To run a backend Python file, type `python3 app.py`, if your Python file is named `app.py` of course.

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

In Gitpod you have superuser security privileges by default. Therefore you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the lessons.

To log into the Heroku toolbelt CLI:

1. Log in to your Heroku account and go to *Account Settings* in the menu under your avatar.
2. Scroll down to the *API Key* and click *Reveal*
3. Copy the key
4. In Gitpod, from the terminal, run `heroku_config`
5. Paste in your API key when asked

You can now use the `heroku` CLI program - try running `heroku apps` to confirm it works. This API key is unique and private to you so do not share it. If you accidentally make it public then you can create a new one with _Regenerate API Key_.

------

## Release History

We continually tweak and adjust this template to help give you the best experience. Here is the version history:

**September 1 2021:** Remove `PGHOSTADDR` environment variable.

**July 19 2021:** Remove `font_fix` script now that the terminal font issue is fixed.

**July 2 2021:** Remove extensions that are not available in Open VSX.

**June 30 2021:** Combined the P4 and P5 templates into one file, added the uptime script. See the FAQ at the end of this file.

**June 10 2021:** Added: `font_fix` script and alias to fix the Terminal font issue

**May 10 2021:** Added `heroku_config` script to allow Heroku API key to be stored as an environment variable.

**April 7 2021:** Upgraded the template for VS Code instead of Theia.

**October 21 2020:** Versions of the HTMLHint, Prettier, Bootstrap4 CDN and Auto Close extensions updated. The Python extension needs to stay the same version for now.

**October 08 2020:** Additional large Gitpod files (`core.mongo*` and `core.python*`) are now hidden in the Explorer, and have been added to the `.gitignore` by default.

**September 22 2020:** Gitpod occasionally creates large `core.Microsoft` files. These are now hidden in the Explorer. A `.gitignore` file has been created to make sure these files will not be committed, along with other common files.

**April 16 2020:** The template now automatically installs MySQL instead of relying on the Gitpod MySQL image. The message about a Python linter not being installed has been dealt with, and the set-up files are now hidden in the Gitpod file explorer.

**April 13 2020:** Added the _Prettier_ code beautifier extension instead of the code formatter built-in to Gitpod.

**February 2020:** The initialisation files now _do not_ auto-delete. They will remain in your project. You can safely ignore them. They just make sure that your workspace is configured correctly each time you open it. It will also prevent the Gitpod configuration popup from appearing.

**December 2019:** Added Eventyret's Bootstrap 4 extension. Type `!bscdn` in a HTML file to add the Bootstrap boilerplate. Check out the <a href="https://github.com/Eventyret/vscode-bcdn" target="_blank">README.md file at the official repo</a> for more options.

------

## FAQ about the uptime script

**Why have you added this script?**

It will help us to calculate how many running workspaces there are at any one time, which greatly helps us with cost and capacity planning. It will help us decide on the future direction of our cloud-based IDE strategy.

**How will this affect me?**

For everyday usage of Gitpod, it doesn’t have any effect at all. The script only captures the following data:

- An ID that is randomly generated each time the workspace is started.
- The current date and time
- The workspace status of “started” or “running”, which is sent every 5 minutes.

It is not possible for us or anyone else to trace the random ID back to an individual, and no personal data is being captured. It will not slow down the workspace or affect your work.

**So….?**

We want to tell you this so that we are being completely transparent about the data we collect and what we do with it.

**Can I opt out?**

Yes, you can. Since no personally identifiable information is being captured, we'd appreciate it if you let the script run; however if you are unhappy with the idea, simply run the following commands from the terminal window after creating the workspace, and this will remove the uptime script:

```
pkill uptime.sh
rm .vscode/uptime.sh
```

**Anything more?**

Yes! We'd strongly encourage you to look at the source code of the `uptime.sh` file so that you know what it's doing. As future software developers, it will be great practice to see how these shell scripts work.

---

Happy coding!
