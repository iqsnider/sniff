use sniff_rust::graph::erdos_renyi_adj;
use sniff_rust::graph::make_laplacian;
use sniff_rust::noise::noise_goe;

fn main() {
    let n = 10;
    let p = 0.3;

    let adj = erdos_renyi_adj(n, p);
    print!("{:?}", adj);
    let l = make_laplacian(&adj);
    print!("{:?}", l);
    let l_noisy = noise_goe(&l, 0.1);
    print!("{:?}", l_noisy);
}
