function studentManagerPanels() {
    const panels = ["Credentials", "Attendance", "Payment"]
    panels.forEach((button) => {
        $(`.${button}Button`).on('shown.bs.collapse', () => {
            panels.forEach((toClose) => {
                if (toClose !== button) {
                    $(`.${toClose}Button`).collapse('hide')
                }
            })
        })
    })
}

document.addEventListener('DOMContentLoaded', () => {
    studentManagerPanels()
})