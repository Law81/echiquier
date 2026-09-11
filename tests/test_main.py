from project_name.main import main


def test_main(capsys) -> None:
    main()
    assert capsys.readouterr().out == "Project is ready.\n"