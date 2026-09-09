function Header() {
  return (
    <header className="site-header">
      <div className="container header-inner">
        <span className="site-title">Stock Market Prediction</span>
        <nav className="site-nav">
          <a href="#predict-section">Predict</a>
          <a href="#charts-section">Charts</a>
          <a href="#results-section">Results</a>
          <a href="#comparison-section">Comparison</a>
        </nav>
      </div>
    </header>
  );
}

export default Header;
