(function(window, undefined) {
  'use strict';

    $(document).ready(function() {

        $('.test').DataTable( {
            "order": [[ 0, "asc" ]]
        } );
    });

})(window);