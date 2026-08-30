import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog.jsx'
import { Settings, Save, Eye, EyeOff, Lock, Unlock } from 'lucide-react'

const AdminPanel = ({ isOpen, onClose }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [password, setPassword] = useState('')
  const [ads, setAds] = useState({
    header: { content: '', enabled: false },
    sidebar: { content: '', enabled: false },
    footer: { content: '', enabled: false },
    between_sections: { content: '', enabled: false }
  })

  const ADMIN_PASSWORD = "admin123" // يمكن تغييرها لاحقاً

  useEffect(() => {
    // تحميل الإعلانات المحفوظة من localStorage
    const savedAds = localStorage.getItem('website_ads')
    if (savedAds) {
      setAds(JSON.parse(savedAds))
    }
  }, [])

  const handleLogin = () => {
    if (password === ADMIN_PASSWORD) {
      setIsAuthenticated(true)
      setPassword('')
    } else {
      alert('كلمة المرور غير صحيحة')
    }
  }

  const handleSaveAds = () => {
    localStorage.setItem('website_ads', JSON.stringify(ads))
    // إرسال حدث لتحديث الإعلانات في الموقع
    window.dispatchEvent(new CustomEvent('adsUpdated', { detail: ads }))
    alert('تم حفظ الإعلانات بنجاح!')
  }

  const updateAd = (location, field, value) => {
    setAds(prev => ({
      ...prev,
      [location]: {
        ...prev[location],
        [field]: value
      }
    }))
  }

  if (!isAuthenticated) {
    return (
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="max-w-md" dir="rtl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Lock className="h-5 w-5" />
              تسجيل دخول الإدارة
            </DialogTitle>
            <DialogDescription>
              يرجى إدخال كلمة المرور للوصول إلى لوحة التحكم
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            <div>
              <Label htmlFor="password">كلمة المرور</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
                placeholder="أدخل كلمة المرور"
              />
            </div>
            <Button onClick={handleLogin} className="w-full">
              <Unlock className="h-4 w-4 mr-2" />
              دخول
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    )
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto" dir="rtl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Settings className="h-6 w-6" />
            لوحة تحكم الإعلانات
          </DialogTitle>
          <DialogDescription>
            يمكنك إدارة الإعلانات في جميع أنحاء الموقع من هنا
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-6">
          {/* إعلان الرأس */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">إعلان الرأس</CardTitle>
              <CardDescription>يظهر في أعلى الموقع</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-2">
                <Button
                  variant={ads.header.enabled ? "default" : "outline"}
                  size="sm"
                  onClick={() => updateAd('header', 'enabled', !ads.header.enabled)}
                >
                  {ads.header.enabled ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
                  {ads.header.enabled ? 'مفعل' : 'معطل'}
                </Button>
              </div>
              <Textarea
                value={ads.header.content}
                onChange={(e) => updateAd('header', 'content', e.target.value)}
                placeholder="أدخل كود HTML للإعلان..."
                rows={4}
              />
            </CardContent>
          </Card>

          {/* إعلان الشريط الجانبي */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">إعلان الشريط الجانبي</CardTitle>
              <CardDescription>يظهر في الجانب الأيمن من الموقع</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-2">
                <Button
                  variant={ads.sidebar.enabled ? "default" : "outline"}
                  size="sm"
                  onClick={() => updateAd('sidebar', 'enabled', !ads.sidebar.enabled)}
                >
                  {ads.sidebar.enabled ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
                  {ads.sidebar.enabled ? 'مفعل' : 'معطل'}
                </Button>
              </div>
              <Textarea
                value={ads.sidebar.content}
                onChange={(e) => updateAd('sidebar', 'content', e.target.value)}
                placeholder="أدخل كود HTML للإعلان..."
                rows={4}
              />
            </CardContent>
          </Card>

          {/* إعلان بين الأقسام */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">إعلان بين الأقسام</CardTitle>
              <CardDescription>يظهر بين أقسام المحتوى</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-2">
                <Button
                  variant={ads.between_sections.enabled ? "default" : "outline"}
                  size="sm"
                  onClick={() => updateAd('between_sections', 'enabled', !ads.between_sections.enabled)}
                >
                  {ads.between_sections.enabled ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
                  {ads.between_sections.enabled ? 'مفعل' : 'معطل'}
                </Button>
              </div>
              <Textarea
                value={ads.between_sections.content}
                onChange={(e) => updateAd('between_sections', 'content', e.target.value)}
                placeholder="أدخل كود HTML للإعلان..."
                rows={4}
              />
            </CardContent>
          </Card>

          {/* إعلان التذييل */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">إعلان التذييل</CardTitle>
              <CardDescription>يظهر في أسفل الموقع</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-2">
                <Button
                  variant={ads.footer.enabled ? "default" : "outline"}
                  size="sm"
                  onClick={() => updateAd('footer', 'enabled', !ads.footer.enabled)}
                >
                  {ads.footer.enabled ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
                  {ads.footer.enabled ? 'مفعل' : 'معطل'}
                </Button>
              </div>
              <Textarea
                value={ads.footer.content}
                onChange={(e) => updateAd('footer', 'content', e.target.value)}
                placeholder="أدخل كود HTML للإعلان..."
                rows={4}
              />
            </CardContent>
          </Card>

          <div className="flex gap-4">
            <Button onClick={handleSaveAds} className="flex-1">
              <Save className="h-4 w-4 mr-2" />
              حفظ التغييرات
            </Button>
            <Button variant="outline" onClick={() => setIsAuthenticated(false)}>
              تسجيل خروج
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

export default AdminPanel

