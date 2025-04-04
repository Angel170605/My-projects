<?php
/*
Plugin Name: Meta Description Manager
Description: Añade y gestiona meta descriptions para SEO en páginas y entradas.
Version: 1.0
Author: Tu Nombre
*/

// Añadir campo meta description en el editor
function mdm_add_meta_description_field() {
    $screens = ['post', 'page'];
    foreach ($screens as $screen) {
        add_meta_box(
            'mdm_meta_description_box',
            'Meta Description',
            'mdm_meta_description_box_html',
            $screen,
            'normal',
            'high'
        );
    }
}
add_action('add_meta_boxes', 'mdm_add_meta_description_field');

// HTML para el campo meta description
function mdm_meta_description_box_html($post) {
    $value = get_post_meta($post->ID, '_mdm_meta_description', true);
    wp_nonce_field('mdm_save_meta_description', 'mdm_meta_description_nonce');
    ?>
    <label for="mdm_meta_description">Descripción para SEO (máx. 160 caracteres):</label><br>
    <textarea id="mdm_meta_description" name="mdm_meta_description" rows="3" style="width:100%; max-width:600px;"><?php echo esc_textarea($value); ?></textarea>
    <p class="description">Esta descripción aparecerá en los resultados de búsqueda.</p>
    <script>
    jQuery(document).ready(function($) {
        $('#mdm_meta_description').on('input', function() {
            var len = $(this).val().length;
            var remaining = 160 - len;
            $('.mdm-counter').remove();
            $(this).after('<p class="description mdm-counter">Caracteres: ' + len + ' (Restantes: ' + remaining + ')</p>');
            if (remaining < 0) {
                $('.mdm-counter').css('color', 'red');
            }
        }).trigger('input');
    });
    </script>
    <?php
}

// Guardar el campo meta description
function mdm_save_meta_description($post_id) {
    if (!isset($_POST['mdm_meta_description_nonce']) || 
        !wp_verify_nonce($_POST['mdm_meta_description_nonce'], 'mdm_save_meta_description')) {
        return;
    }
    
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }
    
    if (!current_user_can('edit_post', $post_id)) {
        return;
    }
    
    if (isset($_POST['mdm_meta_description'])) {
        update_post_meta(
            $post_id,
            '_mdm_meta_description',
            sanitize_text_field($_POST['mdm_meta_description'])
        );
    }
}
add_action('save_post', 'mdm_save_meta_description');

// Mostrar la meta description en el front-end
function mdm_add_meta_description_to_head() {
    if (is_singular()) {
        global $post;
        $meta_description = get_post_meta($post->ID, '_mdm_meta_description', true);
        
        if (!empty($meta_description)) {
            echo '<meta name="description" content="' . esc_attr($meta_description) . '" />' . "\n";
        }
    }
}
add_action('wp_head', 'mdm_add_meta_description_to_head', 1);