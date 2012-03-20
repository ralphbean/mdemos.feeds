<%namespace name="tw" module="moksha.utils.mako"/>
<div id="${tw._('id')}" class="moksha-feedreader">
  <script>
    moksha_feed_topic = '${tw._('topic')}';
  </script>
  <div id="LeftPane">
    ${tw._('feed_tree').display()}
  </div>
  <div id="RightPane">
    <div id="TopPane">
      ${tw._('feed_entries_tree').display()}
    </div>
    <div id="BottomPane"></div>
  </div>
</div>
