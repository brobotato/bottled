def generate_message(message):
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link href="/static/message.css" rel="stylesheet">
        <title>Write a message</title>
    </head>
    <div id="scroll">
        <input class="submit" id="left" type="image" src="static/scroll.png"/>
        <div id="textdiv">
            <p class="text" id="text">{0}</p>
        </div>
        <input class="submit" id="right" type="image" src="static/scroll.png"/>
    </div>
    </body>
    </html>
    """.format(message[0])