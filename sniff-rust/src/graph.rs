use faer::{rand::{self, Rng}, Mat};

pub fn erdos_renyi_adj(n: usize, p: f64) -> Mat<f64> {
    let mut mat = Mat::zeros(n, n);
    let mut rng = rand::rng();

    for i in 1..n {
        for j in (i+1)..n {
            let e = f64::from(rng.random_bool(p) as u8);

            mat[(i, j)] = e;
            mat[(j, i)] = e;
        }
    }

    mat
}

pub fn make_laplacian(mat: &Mat<f64>) -> Mat<f64> {
    assert_eq!(mat.nrows(), mat.ncols(), "matrix must be square");

    Mat::from_fn(mat.nrows(), mat.ncols(), |i, j| (
        if i == j {
            mat.row(i).sum()
        } else {
            -mat[(i, j)]
        }
    ))
}

