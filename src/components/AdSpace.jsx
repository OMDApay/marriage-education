import { useState, useEffect } from 'react'

const AdSpace = ({ location, className = "" }) => {
  const [adContent, setAdContent] = useState('')
  const [isEnabled, setIsEnabled] = useState(false)

  useEffect(() => {
    // تحميل الإعلانات من localStorage
    const loadAds = () => {
      const savedAds = localStorage.getItem('website_ads')
      if (savedAds) {
        const ads = JSON.parse(savedAds)
        if (ads[location]) {
          setAdContent(ads[location].content || '')
          setIsEnabled(ads[location].enabled || false)
        }
      }
    }

    loadAds()

    // الاستماع لتحديثات الإعلانات
    const handleAdsUpdate = (event) => {
      const ads = event.detail
      if (ads[location]) {
        setAdContent(ads[location].content || '')
        setIsEnabled(ads[location].enabled || false)
      }
    }

    window.addEventListener('adsUpdated', handleAdsUpdate)
    return () => window.removeEventListener('adsUpdated', handleAdsUpdate)
  }, [location])

  if (!isEnabled || !adContent) {
    return null
  }

  return (
    <div className={`ad-space ad-${location} ${className}`}>
      <div 
        dangerouslySetInnerHTML={{ __html: adContent }}
        className="w-full"
      />
    </div>
  )
}

export default AdSpace

