
# Dispy
 
If you want to play RPG, this is your guy! A bot for your Discord server.
* Chose your path.
* Add your own stories.
* Customize classes.
* Roll dices.

## How to use it

1. Set up your Bot Application from [Discord Developer Portal](https://guide.pycord.dev/getting-started/creating-your-first-bot).
2. Clone the repo: 
    ```sh
    git clone https://github.com/melosamuel/Dispy.git
    ```
3. Go to repo's folder and set up a virtual environment:
    ```sh
    python.exe -m venv venv
    ./venv/Scripts/activate
    ```
4. Install the requirements:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the bot:
    ```sh
    python.exe src
    ```
## Commands
### !add_story
To add new stories, you need a JSON file structured this way:
```
{ 
    name: The story's name,
    resume: The story's synopsis,
    progresses: [
        A list that holds all points of the story.
        {
            description: The message. It's like what the master says to continue the game,
            choices:[
                A list that holds possible ilimited choices for the player.
                {
                    title: Title of the option,
                    response: A response for this choice.
                }
            ]
        },
        {
            ...
        }
    ]

}
```
