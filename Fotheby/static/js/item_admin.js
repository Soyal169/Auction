// static/js/item_admin.js
(function($){
    $(document).ready(function(){
        $('#id_category').change(function(){
            var selectedCategory = $(this).val();

            // Hide all sections
            $('.drawing-section, .painting-section, .image-section, .sculpture-section, .carving-section').hide();

            // Show the section based on the selected category
            if (selectedCategory === 'Drawings') {
                $('.drawing-section').show();
            } else if (selectedCategory === 'Paintings') {
                $('.painting-section').show();
            } else if (selectedCategory === 'Photographic Images') {
                $('.image-section').show();
            } else if (selectedCategory === 'Sculptures') {
                $('.sculpture-section').show();
            } else if (selectedCategory === 'Carvings') {
                $('.carving-section').show();
            }
        });
    });
})(django.jQuery);
