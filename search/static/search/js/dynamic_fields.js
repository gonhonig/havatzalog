    $(document).ready(function () {
        var next = 1;
        $(".add-more").click(function(e){
            e.preventDefault();
            var addto = "#field" + next;
            var addRemove = "#field" + (next);
            next = next + 1;
            var newIn = '<select class="form-control" name="operator' + next + '" id="operator' + next + '"><option value="and">וגם</option><option value="or">או</option></select><select class="form-control mr-sm-2 picker" name="select' + next + '" id="select' + next + '" x-placement="בחר שדה"><option value="pupil__name__contains">חניך</option><option value="tags__name__in">תגיות</option><option value="parameter__name__contains">פרמטר</option><option class="pick-date" value="updated_time__range">תאריכים</option><option value="details__contains">תוכן</option></select><input autocomplete="off" class="form-control mr-sm-2 input-width" id="field' + next + '" name="field' + next + '" type="text" placeholder="מילת חיפוש נוספת"/>';
            var newInput = $(newIn);
            var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger btn-sm remove-me  mr-sm-2" ><span class="oi oi-minus"></button></div><div id="field" class="margin-top-05">';
            var removeButton = $(removeBtn);
            $(addto).after(newInput);
            $(addRemove).after(removeButton);
            $("#field" + next).attr('data-source',$(addto).attr('data-source'));
            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#field" + fieldNum;
                var selectID = "#select" + fieldNum;
                var operatorID = "#operator" + fieldNum;
                $(this).remove();
                $(fieldID).remove();
                $(selectID).remove();
                $(operatorID).remove();
            });
            $('.picker').change(putDatePicker);
        });
        $('.picker').change(putDatePicker);

        function putDatePicker (e) {
            e.preventDefault();
            var fieldNum = this.id.charAt(this.id.length-1);
            var fieldID = "#field" + fieldNum;
            if (this.value == 'updated_time__range'){
                $(fieldID).daterangepicker({
                    "opens": "left",
                    "autoApply": true,
                    locale: {
                      format: 'YYYY/MM/DD'
                    },
                });
            }
        }
    });


// $('.date-picker').daterangepicker();