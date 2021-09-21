<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
        <style>
            thead {text-align: center}
            td.like:hover {background: rgb(225, 240, 181)}
            td.maybe:hover {background: rgb(252, 253, 177)}
            td.dislike:hover {background: rgb(250, 217, 210)}
            div.hackernews {text-align: right; font-size: x-large; padding-right: 10px;}
        </style>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/" class="ui left floated small primary button">Home 🏠</a>
                        <a href="/clear" class="ui left floated small primary button">Clear records 🧹</a>
                        <div class="hackernews">🌏 Hacker News 👨‍💻</div>
                    </th>
                </tr>
            </thead>
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>Points</th>
                <th>Comments</th>
                <th colspan="3">Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }} " target="_blank">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td class="like"><a href="/add_label/?label=like&id={{ row.id }}">✅</a></td>
                    <td class="maybe"><a href="/add_label/?label=maybe&id={{ row.id }}">🤔</a></td>
                    <td class="dislike"><a href="/add_label/?label=dislike&id={{ row.id }}">❌</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
