(function() {
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function (mutation) {
            var added = mutation.addedNodes;
            for ( var node, i = added.length; (node = added[--i]); ) {
                if(!node.querySelectorAll){continue;}
                var els = node.querySelectorAll('div[id$="_hotjar_branding"]');
                if(els.length){
                    els[0].parentNode.removeChild(els[0]);
                    observer.disconnect();
                }
            }
        });
    });
    observer.observe(document, { childList: true, subtree : true });
})();
