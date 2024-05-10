def generate_bash_for_subject(
    subject: str,
    dir_bids: str,
    dir_deriv: str,
    dir_work: str,
    dir_sub_work: str
) -> str:
    """
    Generate bash script for processing a subject.

    Args:
        subject (str): Subject ID.
        dir_bids (str): BIDS directory path.
        dir_deriv (str): Derivatives directory path.
        dir_work (str): Working directory path.
        dir_sub_work (str): Subject's working directory path.

    Returns:
        str: Generated bash script.

    """
    return f'echo "Subject: {subject}"\n' +\
        'echo "Clearing fmriprep working directory..."\n' +\
        f'rm -rf {dir_sub_work}\n\n' +\
        'singularity run --cleanenv -B ' +\
        f'{dir_bids}/,{dir_deriv}/,{dir_work}/,' +\
        '/afs/cbs/software/freesurfer/ ' +\
        '/data/p_SoftwareServiceLinux_sc/fmriprep/22.0.1/1 ' +\
        f'{dir_bids}/ {dir_deriv}/ ' +\
        f'participant --participant-label {subject.split("-")[1]} ' +\
        '--use-aroma --output-spaces T1w MNI152NLin6Asym ' +\
        '--dummy-scans 0 --fs-license-file /afs/cbs/software/freesurfer/licensekeys ' +\
        f'--fs-no-reconall -w {dir_sub_work} --clean-workdir ' +\
        '--write-graph --stop-on-first-crash --notrack --verbose --skip-bids-validation\n\n' +\
        'echo "Fmriprep done. Removing fmriprep working directory..."\n' +\
        f'rm -rf {dir_sub_work}\n\n'