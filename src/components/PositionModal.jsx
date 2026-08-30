import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { X, Heart, Star, Info } from 'lucide-react'
import { assetPath } from '@/lib/assetPath.js'

const PositionModal = ({ position, isOpen, onClose }) => {
  if (!position) return null

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto" dir="rtl">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle className="text-2xl text-blue-700 flex items-center gap-2">
              <Heart className="h-6 w-6 text-pink-500" />
              {position.title}
            </DialogTitle>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
          <DialogDescription className="text-lg text-gray-600">
            {position.category}
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-6">
          {position.image && (
            <div className="text-center">
              <img 
                src={assetPath(position.image)} 
                alt={position.title}
                className="mx-auto rounded-lg shadow-lg max-w-full h-auto"
                style={{maxHeight: '300px'}}
              />
            </div>
          )}
          
          <div className="bg-blue-50 p-4 rounded-lg border-r-4 border-blue-400">
            <h3 className="text-lg font-semibold text-blue-800 mb-2 flex items-center gap-2">
              <Info className="h-5 w-5" />
              الوصف
            </h3>
            <p className="text-blue-700 leading-relaxed">
              {position.description}
            </p>
          </div>
          
          {position.benefits && (
            <div className="bg-green-50 p-4 rounded-lg border-r-4 border-green-400">
              <h3 className="text-lg font-semibold text-green-800 mb-3 flex items-center gap-2">
                <Star className="h-5 w-5" />
                الفوائد والمميزات
              </h3>
              <ul className="space-y-2">
                {position.benefits.map((benefit, index) => (
                  <li key={index} className="text-green-700 flex items-start gap-2">
                    <span className="text-green-500 mt-1">•</span>
                    {benefit}
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {position.tips && (
            <div className="bg-yellow-50 p-4 rounded-lg border-r-4 border-yellow-400">
              <h3 className="text-lg font-semibold text-yellow-800 mb-3">
                نصائح مهمة
              </h3>
              <ul className="space-y-2">
                {position.tips.map((tip, index) => (
                  <li key={index} className="text-yellow-700 flex items-start gap-2">
                    <span className="text-yellow-500 mt-1">•</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {position.warnings && (
            <div className="bg-red-50 p-4 rounded-lg border-r-4 border-red-400">
              <h3 className="text-lg font-semibold text-red-800 mb-3">
                تحذيرات واحتياطات
              </h3>
              <ul className="space-y-2">
                {position.warnings.map((warning, index) => (
                  <li key={index} className="text-red-700 flex items-start gap-2">
                    <span className="text-red-500 mt-1">⚠</span>
                    {warning}
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {position.tags && (
            <div className="flex flex-wrap gap-2">
              {position.tags.map((tag, index) => (
                <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-800">
                  {tag}
                </Badge>
              ))}
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}

export default PositionModal

