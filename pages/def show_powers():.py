def show_powers():
    power_names = [
        power.name for power in ...
    ]

    icon_row = row(10)

    for power_name in power_names:
        icon = ....
        icon_row.link_button(
            icon,
            f"https://arnaudmiribel.github.io/streamlit-extras/extras/{power_name}/",
            help=description,
            use_container_width=True,
        )
