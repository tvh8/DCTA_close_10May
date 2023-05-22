document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['interaction', 'dayGrid', 'timeGrid', 'list'],
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        defaultDate: '2023-05-19',
        navLinks: true, // can click day/week names to navigate views
        selectable: true,
        selectMirror: true,
        select: function(arg) {
            // code to run when a date range is selected
        },
        eventLimit: true, // allow "more" link when too many events
        events: [
            // your event data here
        ]
    });

    calendar.render();
});
