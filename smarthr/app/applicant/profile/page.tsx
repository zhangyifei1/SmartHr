"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { getUserInfo, updateUserInfo } from "@/lib/api";
import { toast } from "sonner";
import { User, Mail, Phone, Building, Calendar, Edit2, Save, X } from "lucide-react";

interface UserInfo {
  id: string;
  name: string;
  email: string;
  phone?: string;
  company?: string;
  role: string;
  createdAt: string;
}

export default function ApplicantProfilePage() {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [editForm, setEditForm] = useState({
    name: "",
    phone: "",
    email: "",
  });

  useEffect(() => {
    loadUserInfo();
  }, []);

  const loadUserInfo = async () => {
    try {
      setIsLoading(true);
      const data = await getUserInfo();
      setUserInfo(data);
      setEditForm({
        name: data.name || "",
        phone: data.phone || "",
        email: data.email || "",
      });
    } catch (error) {
      toast.error("加载用户信息失败");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      await updateUserInfo({
        name: editForm.name,
        phone: editForm.phone,
        email: editForm.email,
      });
      toast.success("个人信息更新成功");
      setIsEditing(false);
      loadUserInfo();
    } catch (error) {
      toast.error("更新失败，请重试");
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    if (userInfo) {
      setEditForm({
        name: userInfo.name || "",
        phone: userInfo.phone || "",
        email: userInfo.email || "",
      });
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">加载中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">个人中心</h1>
          <p className="mt-2 text-gray-600">管理您的个人信息和账户设置</p>
        </div>

        {/* 个人信息卡片 */}
        <Card className="mb-6">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-xl flex items-center gap-2">
                <User className="h-5 w-5" />
                基本信息
              </CardTitle>
              <CardDescription>查看和编辑您的个人资料</CardDescription>
            </div>
            {!isEditing && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsEditing(true)}
                className="flex items-center gap-1"
              >
                <Edit2 className="h-4 w-4" />
                编辑
              </Button>
            )}
          </CardHeader>
          <CardContent>
            {isEditing ? (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">
                      姓名 <span className="text-red-500">*</span>
                    </Label>
                    <Input
                      id="name"
                      value={editForm.name}
                      onChange={(e) =>
                        setEditForm({ ...editForm, name: e.target.value })
                      }
                      placeholder="请输入姓名"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="phone">手机号码</Label>
                    <Input
                      id="phone"
                      value={editForm.phone}
                      onChange={(e) =>
                        setEditForm({ ...editForm, phone: e.target.value })
                      }
                      placeholder="请输入手机号码"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">
                    邮箱 <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    value={editForm.email}
                    onChange={(e) =>
                      setEditForm({ ...editForm, email: e.target.value })
                    }
                    placeholder="请输入邮箱地址"
                  />
                </div>
                <div className="flex justify-end gap-3 pt-4">
                  <Button
                    variant="outline"
                    onClick={handleCancel}
                    disabled={isSaving}
                    className="flex items-center gap-1"
                  >
                    <X className="h-4 w-4" />
                    取消
                  </Button>
                  <Button
                    onClick={handleSave}
                    disabled={isSaving}
                    className="flex items-center gap-1"
                  >
                    <Save className="h-4 w-4" />
                    {isSaving ? "保存中..." : "保存"}
                  </Button>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <User className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">姓名</p>
                    <p className="font-medium text-gray-900">
                      {userInfo?.name || "-"}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                    <Mail className="h-5 w-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">邮箱</p>
                    <p className="font-medium text-gray-900">
                      {userInfo?.email || "-"}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                    <Phone className="h-5 w-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">手机号码</p>
                    <p className="font-medium text-gray-900">
                      {userInfo?.phone || "-"}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center">
                    <Calendar className="h-5 w-5 text-orange-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">注册时间</p>
                    <p className="font-medium text-gray-900">
                      {userInfo?.createdAt
                        ? new Date(userInfo.createdAt).toLocaleDateString(
                            "zh-CN"
                          )
                        : "-"}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* 账户安全卡片 */}
        <Card>
          <CardHeader>
            <CardTitle className="text-xl flex items-center gap-2">
              <Building className="h-5 w-5" />
              账户安全
            </CardTitle>
            <CardDescription>管理您的账户安全设置</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b border-gray-100">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <Mail className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">邮箱验证</p>
                    <p className="text-sm text-gray-500">
                      {userInfo?.email ? "已验证" : "未验证"}
                    </p>
                  </div>
                </div>
                <Button variant="outline" size="sm">
                  修改邮箱
                </Button>
              </div>
              <div className="flex items-center justify-between py-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                    <Building className="h-5 w-5 text-green-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">密码</p>
                    <p className="text-sm text-gray-500">建议定期更换密码</p>
                  </div>
                </div>
                <Button variant="outline" size="sm">
                  修改密码
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
