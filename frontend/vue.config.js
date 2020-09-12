module.exports = {
    lintOnSave: process.env.NODE_ENV !== 'production',
    devServer: {
      proxy: 'http://localhost:5000'
    }

  }

