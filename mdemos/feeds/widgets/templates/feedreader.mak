<div id="${id}" class="moksha-feedreader">
  <script>
    moksha_feed_topic = '${topic}';
  </script>
  <div id="LeftPane">
    ${c.feed_tree()}
  </div>
  <div id="RightPane">
    <div id="TopPane">
      ${c.feed_entries_tree()}
    </div>
    <div id="BottomPane"></div>
  </div>
</div>
