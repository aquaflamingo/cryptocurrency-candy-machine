package com.robertsimoes.pos_android

import android.os.Bundle
import android.os.Handler
import android.support.v7.app.AppCompatActivity
import android.webkit.CookieManager
import android.webkit.WebView
import android.webkit.WebResourceRequest
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import android.webkit.WebViewClient
import android.os.Looper
import android.widget.Button
import android.widget.Toast
import android.widget.Toast.LENGTH_SHORT


private const val TEN_SECONDS_MS: Long = 100000
private const val AIRDROPZ_URL = "http://airdropz.xyz"
private const val AIRDROPZ_HOST = "airdropz.xyz"

class MainActivity : AppCompatActivity() {

    private lateinit var myWebView: WebView
    private lateinit var refreshButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        myWebView = findViewById(R.id.webview)
        refreshButton = findViewById(R.id.restart_button)
        myWebView.settings.javaScriptEnabled = true
        val cookieManager = CookieManager.getInstance()
        cookieManager.removeAllCookies(null)
        cookieManager.setAcceptCookie(false)
        cookieManager.setAcceptThirdPartyCookies(myWebView, false)

        myWebView.webViewClient = WebViewController()

        refreshButton.setOnClickListener {
            RestartRunnable().run()
            Toast.makeText(this, "Refreshed!", LENGTH_SHORT).show()

        }
    }


    override fun onResume() {
        myWebView.loadUrl(AIRDROPZ_URL)
        super.onResume()
    }

    inner class WebViewController : WebViewClient() {
        override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
            return false
        }
    }

    inner class RestartRunnable() : Runnable {

        override fun run() {
            runOnUiThread {
                myWebView.clearCache(true)
                myWebView.loadUrl(AIRDROPZ_URL)
            }
        }

    }
}
