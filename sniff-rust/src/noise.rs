use faer::rand::{rng, Rng};
use faer::stats::prelude::StandardNormal;
use faer::Mat;

pub fn noise_goe(laplacian: &Mat<f64>, noise_strength: f64) -> Mat<f64> {
    assert_eq!(laplacian.nrows(), laplacian.ncols(), "matrix must be square");
    let n = laplacian.nrows();
    let mut rng = rng();
    let mut out = laplacian.clone();
    let diag_scale = 2f64.sqrt();

    for i in 0..n {
        let z_diag: f64 = rng.sample(StandardNormal);
        out[(i, i)] += noise_strength * (diag_scale * z_diag);

        for j in (i + 1)..n {
            let z: f64 = rng.sample(StandardNormal);
            let v = noise_strength * z;

            out[(i, j)] += v;
            out[(j, i)] += v;
        }
    }

    out
}

