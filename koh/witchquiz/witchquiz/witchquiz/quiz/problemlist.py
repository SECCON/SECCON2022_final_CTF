from . import purerandom, randomrotate, ec_problem, phase_problem

problemClasses = {
    'purerandom': purerandom.PureRandom(),
    'randomrotate': randomrotate.RandomRotate(),
    'ec': ec_problem.ECProblem(),
    'phase': phase_problem.Phase()
}

