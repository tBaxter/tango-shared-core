// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
var tango_markdown_settings = {
  nameSpace:          'markdown', // Useful to prevent multi-instances CSS conflict
  //previewParserPath:  '~/sets/markdown/preview.php',
  onShiftEnter:       { keepDefault:false, openWith:'\n\n' },
  markupSet: [
    {name:'Bold',      key:'B', openWith:'**', closeWith:'**', className:'icon-bold' },
    {name:'Italic',    key:'I', openWith:'*', closeWith:'*', className:'icon-italic'},
    {name:'Quotes',    key:'Q', openWith:'> ', className:'icon-quote'},
    {name:'Link',
      key:'L',
      openWith:'[',
      closeWith:']([![Link:!:http://]!])',
      placeHolder:'Link',
      className:'icon-link'
    },
    {name:'Bulleted List', openWith:'- ', closeWith:'  ', multiline:true, className:'icon-ul'},
    {
      name:'Numeric List',
      className:'icon-ol',
      multiline:true,
      openWith:function(markItUp) {
        return markItUp.line + '. ';
      }
    },
    {
      name:'Upload photo',
      key:'U',
      className: 'icon-photo icon-add',
      beforeInsert:function() {
        $('#id_image').parent().show();
      }
    },
    {separator:'---------------' },
    { name:'Smileys', className:'emoticon-happy sub-nav', dropMenu: [
        {name:'Big smile', openWith:' :-D ',  className:'emoticon-grin'},
        {name:'Smiley',    openWith:' :-) ',  className:'emoticon-happy'},
        {name:'Neutral',   openWith:' :| ',   className:'emoticon-displeased'},
        {name:'Unhappy',   openWith:' :-( ',  className:'emoticon-unhappy'},
        {name:'Yikes',     openWith:' 8-o ',  className:'emoticon-surprised'},
        {name:'Wink',      openWith:' ;-) ',  className:'emoticon-wink2'},
        {name:'Crazy',     openWith:' :-P ',  className:'emoticon-tongue'},
        {name:'Mad',       openWith:' x-( ',  className:'emoticon-angry'},
        {name:'Cool',      openWith:' 8-) ',  className:'emoticon-sunglasses'},
        {name:'Thumbs up', openWith:':up:',   className:'emoticon-thumbsup'},
        {name:'Devil',     openWith:':devil:', className:'emoticon-devil'},
        {name:'Beer',      openWith:':beer:', className:'emoticon-beer'},
        {name:'Cry',       openWith:':cry:',  className:'emoticon-cry'},
        {name:'Laugh',     openWith:':lol:',  className:'emoticon-laugh'}
      ]
    }
  ]
};


// mIu nameSpace to avoid conflict.
var miu = {
  markdownTitle: function(markItUp, character) {
    var heading = '';
    var n = $.trim(markItUp.selection||markItUp.placeHolder).length;
    for(var i = 0; i < n; i++) {
      heading += character;
    }
    return '\n'+heading+'\n';
  }
};

