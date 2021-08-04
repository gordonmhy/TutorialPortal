function studentManagerPanels() {
    const specifiedPanels = ['Credentials', 'Attendance', 'Payment']
    const mainPanels = ['SelectStudent', 'AddStudent']
    const panelGroups = [specifiedPanels, mainPanels]
    panelGroups.forEach((panels) => {
        panels.forEach((button) => {
            $(`.${button}Button`).on('shown.bs.collapse', () => {
                panels.forEach((toClose) => {
                    if (toClose !== button) {
                        $(`.${toClose}Button`).collapse('hide')
                    }
                })
            })
        })
    })
}

function deleteAttendanceWindows() {
    $('.DeleteAttendanceRecordButton').on('click', () => {
        $('.AttendanceDetailModal').hide()
    })
    $('.DeleteAttendanceRecordRegretButton').on('click', () => {
        $(".modal-backdrop").remove()
        $('body').addClass('modal-open');
    })
}

document.addEventListener('DOMContentLoaded', () => {
    studentManagerPanels()
    deleteAttendanceWindows()
})