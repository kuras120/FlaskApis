// external JS

var $grid = $('.grid').masonry({
    columnWidth: 160,
    itemSelector: '.grid-item',
    fitWidth: true,
    stagger: 30
});

$grid.on( 'click', '.grid-item', function() {
    if ($(window).width() > 768) {
        // change size of item via class
        $(this).toggleClass('grid-item--gigante');
        // trigger layout
        $grid.masonry();
    }
});