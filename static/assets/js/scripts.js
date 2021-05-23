(function(window, undefined) {
  'use strict';

    $(document).ready(function() {

        /**************************************
        *       js of default ordering        *
        **************************************/

        $('.default-ordering2').DataTable( {
            "order": [[ 0, "asc" ]]
        } );

    });

})(window);