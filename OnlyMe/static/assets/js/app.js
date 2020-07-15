function showLoader(status) {
    if (status) {
        $('#loader').removeAttr('hidden');
        $('body').css('cursor', 'wait');
        $('#cover').css({
            'min-height': 'inherit',
            'display': 'flex',
            'flex-direction': 'column',
            'flex': 1,
            'z-index': -1
        });
    } else {
        $('#loader').attr('hidden', 'hidden');
        $('body').css('cursor', 'default');
        $('#cover').removeAttr('style');
    }
}
