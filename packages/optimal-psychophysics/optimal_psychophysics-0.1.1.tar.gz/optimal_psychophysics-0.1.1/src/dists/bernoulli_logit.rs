//! Benroulli logit distribution. Identical to the Bernoulli distribution, but with an internal logit transformation for numerical stability.

//! The Bernoulli distribution `Bernoulli(p)`.

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct BernoulliLogit {
    logit_p: f64,
    dist: rand::distributions::Bernoulli,
}

impl BernoulliLogit {
    /// Construct a new `BernoulliLogit` distribution with the given probability `p`.
    #[inline]
    pub fn new(logit_p: f64) -> Self {
        let p = 1.0 / (1.0 + (-logit_p).exp());
        let dist = rand::distributions::Bernoulli::new(p).unwrap();
        Self { logit_p, dist }
    }

    /// Get the `logit_p` parameter of the distribution.
    #[inline]
    pub fn logit_p(&self) -> f64 {
        self.logit_p
    }
}

impl core::ops::Deref for BernoulliLogit {
    type Target = rand::distributions::Bernoulli;

    fn deref(&self) -> &Self::Target {
        &self.dist
    }
}
