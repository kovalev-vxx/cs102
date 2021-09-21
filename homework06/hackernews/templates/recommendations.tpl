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
                        <div class="hackernews">🌏 Hacker News 👨‍💻</div>
                    </th>
                </tr>
            </thead>
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>Points</th>
                <th>Comments</th>
            </thead>
            
            <thead>
                <th colspan="5">For you</th>
            </thead>
            
            
            <tbody>
                %for row in liked_news:
                <tr>
                    <td><a href="{{ row.url }} " target="_blank">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                </tr>
                %end
            </tbody>
            
            <thead>
                <th colspan="5">May be interesting for you</th>
            </thead>


            <tbody>
                %for row in maybe_news:
                <tr>
                    <td><a href="{{ row.url }} " target="_blank">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                </tr>
                %end
            </tbody>

        </table>
        </div>
    </body>
</html>
