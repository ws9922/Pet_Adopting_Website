$(document).ready(function () {
    $('#pet-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const petID = button.data('source'); // Extract info from data-* attributes
        const content = button.data('content'); // Extract info from data-* attributes

        const modal = $(this);
        if (petID === 'New Pet') {
            modal.find('.modal-title').text(petID);
            $('#pet-form-display').removeAttr('petID');
        } else {
            modal.find('.modal-title').text('Edit Pet ' + petID);
            $('#pet-form-display').attr('petID', petID);
        }

        if (content) {
            modal.find('.form-control').val(content)
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#pet-search-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget)
        const content = button.data('content');
        const modal = $(this);
        if (content) {
            modal.find('.form-control').val(content)
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#pet-match-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget)
        const content = button.data('content');
        const modal = $(this);
        if (content) {
            modal.find('.form-control').val(content)
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#login-modal').on('show.bs.modal', function (event){
        const button = $(event.relatedTarget)
        const content = button.data('content');
        const modal = $(this);
        if (content) {
            modal.find('.form-control-0').val(content)
        } else {
            modal.find('.form-control-0').val('');
        }
    })

    $('#signup-modal').on('show.bs.modal', function (event){
        const button = $(event.relatedTarget)
        const content = button.data('content');
        const modal = $(this);
        if (content) {
            modal.find('.form-control-0').val(content)
        } else {
            modal.find('.form-control-0').val('');
        }
    })

    $('#user-signup').click(function () {
        const UID = $('#signup-modal').find('.form-control-0').val()
        const Password_1 = $('#signup-modal').find('.form-control-1').val()
        const Password_2 = $('#signup-modal').find('.form-control-2').val()
        //result = Password_1.localeCompare(Password_2)

        console.log($('#signup-modal').find('.form-control-0').val());
        $.ajax({
            type: 'POST',
            url: '/signup',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'UID': UID,
                'Password': Password_1
            }),
            success: function (res) {
                console.log(res.response)
                location.reload()
            },
            error: function () {
                console.log('Error');
            },
        });
    });

    $('#user-login').click(function () {
        const UID = $('#login-modal').find('.form-control-0').val()
        const Password = $('#login-modal').find('.form-control-1').val()
        console.log($('#login-modal').find('.form-control-0').val());
        $.ajax({
            type: 'POST',
            url: '/login',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'UID': UID,
                'Password': Password
            }),
            success: function (res) {
                console.log(res.response)
                location.reload()
            },
            error: function () {
                console.log('Error');
            },
        });
    });

    $('#user-logout').click(function () {
        $.ajax({
            type: 'POST',
            url: '/logout',
            success: function (res) {
                console.log(res.response)
                location.reload()
            },
            error: function () {
                console.log('Error');
            },
        });
    });

    $('#submit-pet').click(function () {
        const tID = $('#pet-form-display').attr('petID');
        console.log($('#pet-modal').find('.form-control-0').val());
        $.ajax({
            type: 'POST',
            url: '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'pet_id': $('#pet-modal').find('.form-control-0').val(),
                'pet_type': $('#pet-modal').find('.form-control-1').val(),
                'pet_color': $('#pet-modal').find('.form-control-2').val(),
                'pet_cond': $('#pet-modal').find('.form-control-3').val(),
                'pet_uid': $('#pet-modal').find('.form-control-4').val(),
                'pet_loc': $('#pet-modal').find('.form-control-5').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this);
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    $('.state').click(function () {
        const state = $(this);
        const tID = state.data('source');
        var new_state="";
        if (state.text() === "Normal") {
            new_state = "Sick";
        } else if (state.text() === "Sick") {
            new_state = "Normal";
        } 
        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'pet_condition': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#search-pet').click(function () {
        const pet_ID = $('#pet-search-modal').find('.form-control').val()
        console.log($('#pet-search-modal').find('.form-control').val());
        $.ajax({
            type: 'POST',
            url: '/search',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'search_id': pet_ID
            }),
            success: function (res) {
                console.log(res.response)
                location.href = "search"
            },
            error: function () {
                console.log('Error');
            },
        });
    });

    $('#match-pet').click(function () {
        const UID = $('#pet-match-modal').find('.form-control').val()
        const fav = $('#pet-match-modal').find('.form-control1').val()
        console.log($('#pet-match-modal').find('.form-control').val());
        $.ajax({
            type: 'POST',
            url: '/match',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'search_id': UID,
                'fav': fav
            }),
            success: function (res) {
                console.log(res.response)
                location.href = "match"
            },
            error: function () {
                console.log('Error');
            },
        });
    });

    $('#user-favor').click(function () {
        $.ajax({
            type: 'POST',
            url: '/match',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'search_id': '000',
                'fav': '1'
            }),
            success: function (res) {
                console.log(res.response)
                location.href = "match"
            },
            error: function () {
                console.log('Error');
            },
        });
    });
    
});